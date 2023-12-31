#!/usr/bin/env python3
import sys, json, linecache, tkinter, os
from math import gcd

def display_string(Str):
    root = tkinter.Tk()
    root.geometry("1280x720")
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM,fill=tkinter.X)
    SV = tkinter.Scrollbar(root)
    SV.pack(side = tkinter.RIGHT, fill = tkinter.Y)
    SH = tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL)
    T = tkinter.Text(root, height=1000, width=1000, relief='flat',yscrollcommand=SV.set,xscrollcommand=SH.set,wrap=tkinter.NONE)
    T.insert(tkinter.END, Str)
    T.config(state=tkinter.DISABLED)
    T.pack(side=tkinter.TOP,fill=tkinter.BOTH)
    SV.config(command=T.yview)
    SH.pack(side=tkinter.TOP, fill = tkinter.X)
    SH.config(command=T.xview)

    def copy():
        root.clipboard_clear()
        root.clipboard_append(Str)
        B["text"] = "Copied!"
        root.update()

    frame2 = tkinter.Frame(frame)
    frame2.pack(side=tkinter.BOTTOM)
    B = tkinter.Button(frame2,text="Copy to clipboard", command=copy)
    B.pack(side = tkinter.LEFT)
    warning = tkinter.Label(frame2,text="Please paste before closing window. Esc to exit.")
    warning.pack(side = tkinter.RIGHT)
    root.bind("<Escape>",lambda e: root.destroy())
    tkinter.mainloop()

# Extracted from
# https://stackoverflow.com/questions/66192894/precise-determinant-of-integer-nxn-matrix
def det(M):
    M = [row[:] for row in M] # make a copy to keep original M unmodified
    N, sign, prev = len(M), 1, 1
    for i in range(N-1):
        if M[i][i] == 0: # swap with another row having nonzero i's elem
            swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
            if swapto is None:
                return 0 # all M[*][i] are zero => zero determinant
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i+1,N):
            for k in range(i+1,N):
                # assert ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % prev == 0
                M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) // prev
        prev = M[i][i]
    return sign * M[-1][-1]

def get_base_used_and_intersection_matrix(graph_info, config_info):

    real_graph = graph_info["graph"]
    real_exceptionals = graph_info["blps"]
    real_selfint = graph_info["selfint"]

    selfint = list(real_selfint) #deep copy
    exceptionals = list(real_exceptionals) #deep copy
    Intersection_Matrix = [len(real_graph)*[0] for i in range(len(real_graph))]
    count_graph = [len(real_graph)*[0] for i in range(len(real_graph))]
    for i in range(len(real_graph)):
        for x in real_graph[i]:
            count_graph[i][x] += 1
    for i in exceptionals[::-1]:
        for a in range(len(real_graph)):
            selfint[a] += count_graph[i][a]*count_graph[i][a]
            for b in range(a+1,len(real_graph)):
                count_graph[a][b] += count_graph[i][a]*count_graph[i][b]
                count_graph[b][a] += count_graph[i][a]*count_graph[i][b]
            count_graph[a][i] = 0
            count_graph[i][a] = 0
        selfint[i] = 0
    for a in range(len(real_graph)):
        for b in range(len(real_graph)):
            if a == b:
                Intersection_Matrix[a][b] = selfint[a]
            else:
                Intersection_Matrix[a][b] = count_graph[a][b]

    used = config_info["used"]
    base_used = []
    for i in used:
        if i not in exceptionals:
            base_used.append(i)
    base_used = sorted(base_used)
    a = 0
    used_matrix = [len(base_used)*[0] for i in range(len(base_used))]
    for x in range(len(Intersection_Matrix)):
        if x not in base_used:
            continue
        b = 0
        for y in range(len(Intersection_Matrix[x])):
            if y not in base_used:
                continue
            used_matrix[a][b] = Intersection_Matrix[x][y]
            b += 1
        a += 1
    return base_used, used_matrix

def single_chain(graph_info, config_info):
    base_used, matrix = get_base_used_and_intersection_matrix(graph_info, config_info)
    global_name_dict = graph_info["name"]
    discrepancies = config_info["disc"]
    chain = config_info["chain"]
    used_curves = config_info["used"]
    self_int = config_info["selfint"]

    name_dict = [global_name_dict[used_curves[i]] for i in range(len(used_curves))]

    n = config_info["N"]
    a = min(-discrepancies[chain[0]],-discrepancies[chain[-1]])

    K2 = config_info["K2"]

    S = (
    "\\noindent\n"
    "$\\rule{{12.5cm}}{{1.1pt}}$\n"
    "\\noindent\n"
    "\n"
    "\\textbf{{(...)}} "
    "$K^2={K2}$ - "
    "$\\{{{used_curves}\\}}$ - "
    # "$\\operatorname{{det}}={det}$ - "
    "{intersections} - "
    "{chains}\n\n"
    "\\noindent\n"
    "$\\rule{{12.5cm}}{{1.1pt}}$\n"
    "\\noindent\n"
    )

    COMMA = ",\\allowbreak "

    used_curves_string = ",~\\allowbreak ".join(name_dict)
    chains = "$({n},{a}) : [{SI}]$".format(n=n,a=a,SI=",\\allowbreak ".join([str(-self_int[i]) for i in chain]))

    ignored_blowups = []
    if config_info["en"] != 0:
        ignored_blowups = [(config_info["ea"], config_info["eb"]), (config_info["eb"], config_info["ea"])]

    intersections = []
    for x,y in config_info["blps"]:
        if (x,y) not in ignored_blowups and (y,x) not in ignored_blowups:
            intersections.append(f"$~{name_dict[x]} \\cap {name_dict[y]}$")
        else:
            ignored_blowups.remove((x,y))
            ignored_blowups.remove((y,x))

    if config_info["en"] != 0:
        intersections.append(f"$[{COMMA.join(config_info['en']*['2'])},1] \\times ~{name_dict[config_info['ea']]} \\cap {name_dict[config_info['eb']]}$")

    return S.format(K2=K2, det=det(matrix), used_curves=used_curves_string, intersections=", ".join(intersections), chains=chains)

    # S = f"\\subsection{{Example with \\(K^2={K2}\\)}}\n"

    # S += "This example uses the following curves:\n"
    # S += "\\[" + ",~".join(name_dict) +".\\]\n"

    # S += f"The determinant of their intersection matrix is ${det(matrix)}$. Requires blow ups at the following points:\n"

    # S += "\\[" + ",~".join((f"{name_dict[c[0]]} \\cap {name_dict[c[1]]}" for c in config_info["blps"])) + ".\\]\n"

    # if config_info["en"] != 0:
    #     S += "It also needs extra blow ups at:\n"
    #     S += "\\[{0} \\times ({1} \\cap {2})".format(
    #             config_info["en"],
    #             name_dict[config_info["ea"]],
    #             name_dict[config_info["eb"]]
    #         )

    # S += f"The resulting chain is a $(n,a) = ({n},{a})$.\n"

    # return S


def double_chain(graph_info, config_info):
    base_used, matrix = get_base_used_and_intersection_matrix(graph_info, config_info)
    global_name_dict = graph_info["name"]
    discrepancies = config_info["disc"]
    chain0 = config_info["chain0"]
    chain1 = config_info["chain1"]
    used_curves = config_info["used"]
    self_int = config_info["selfint"]

    name_dict = [global_name_dict[used_curves[i]] for i in range(len(used_curves))]

    n0 = config_info["N0"]
    n1 = config_info["N1"]
    a0 = min(-discrepancies[chain0[0]],-discrepancies[chain0[-1]])
    a1 = min(-discrepancies[chain1[0]],-discrepancies[chain1[-1]])

    K2 = config_info["K2"]


    S = (
    "\\noindent\n"
    "$\\rule{{12.5cm}}{{1.1pt}}$\n"
    "\\noindent\n\n"

    # "\\begin{{fcolorbox}}\n"

    "\\textbf{{(...)}} "
    "$K^2={K2}$ - "
    "$\\{{{used_curves}\\}}$ - "
    # "$\\operatorname{{det}}={det}$ - "
    "{intersections} - "
    "{chains}\n\n"

    # "\\end{{fcolorbox}}\n"

    "\\noindent\n"
    "$\\rule{{12.5cm}}{{1.1pt}}$\n"
    "\\noindent\n"
    )

    COMMA = ",\\allowbreak "

    used_curves_string = ",~\\allowbreak ".join(name_dict)
    chains = "$({n},{a}) : [{SI}]$, ".format(n=n0,a=a0,SI=",\\allowbreak ".join([str(-self_int[i]) for i in chain0]))
    chains += "$({n},{a}) : [{SI}]$".format(n=n1,a=a1,SI=",\\allowbreak ".join([str(-self_int[i]) for i in chain1]))

    ignored_blowups = []
    if config_info["en0"] != 0:
        ignored_blowups = [(config_info["ea0"], config_info["eb0"]), (config_info["eb0"], config_info["ea0"])]
    if config_info["en1"] != 0:
        ignored_blowups += [(config_info["ea1"], config_info["eb1"]), (config_info["eb1"], config_info["ea1"])]

    intersections = []
    for x,y in config_info["blps"]:
        if (x,y) not in ignored_blowups and (y,x) not in ignored_blowups:
            intersections.append(f"$~{name_dict[x]} \\cap {name_dict[y]}$")
        else:
            ignored_blowups.remove((x,y))
            ignored_blowups.remove((y,x))

    if config_info["en0"] != 0:
        intersections.append(f"$[{COMMA.join(config_info['en0']*['2'])},1] \\times ~{name_dict[config_info['ea0']]} \\cap {name_dict[config_info['eb0']]}$")
    if config_info["en1"] != 0:
        intersections.append(f"$[{COMMA.join(config_info['en1']*['2'])},1] \\times ~{name_dict[config_info['ea1']]} \\cap {name_dict[config_info['eb1']]}$")

    if config_info["WH"] != 0:
        # P-extremal.
        Left = []
        for x in chain0[::-1]:
            if x >= len(used_curves):
                Left.append(str(-self_int[x]))
            else:
                A = name_dict[x]
                break
        Right = []
        for x in chain1:
            if x >= len(used_curves):
                Right.append(str(-self_int[x]))
            else:
                B = name_dict[x]
                break
        Total_blowup = Left[::-1] + ['1'] + Right
        intersections.append(f"$[{COMMA.join(Total_blowup)}] \\times ~{A} \\cap {B}$")

    return S.format(K2=K2, det=det(matrix), used_curves=used_curves_string, intersections=", ".join(intersections), chains=chains)

    # S = f"\\subsection{{Example with \\(K^2={K2}\\)}}\n"

    # S += "This example uses the following curves:\n"
    # S += "\\[" + ",~".join(name_dict) +".\\]\n"

    # S += f"The determinant of their intersection matrix is ${det(matrix)}$. Requires blow ups at the following points:\n"

    # S += "\\[" + ",~".join((f"{name_dict[c[0]]} \\cap {name_dict[c[1]]}" for c in config_info["blps"])) + ".\\]\n"

    # if config_info["en0"] != 0 or config_info["en1"] != 0:
    #     S += "It also needs extra blow ups at:\n"
    #     S += "\\[" + ",\\quad ".join(("{0} \\times ({1} \\cap {2})".format(
    #             config_info[f"en{c}"],
    #             name_dict[config_info[f"ea{c}"]],
    #             name_dict[config_info[f"eb{c}"]]
    #         ) for c in range(2) if config_info[f"en{c}"] != 0)
    #     ) + ".\\]\n"

    # S += f"The resulting chains are  $(n_1,a_1) = ({n0},{a0})$ and $(n_2,a_2) = ({n1},{a1})$. This example satisfies $\\gcd(n_1,n_2) = {gcd(n0,n1)}$.\n"

    # return S

def main():

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    PATH = "data"

    K2 = [10,11,12,13,14,15,16,17,18,19]

    body = ""

    for filename in os.listdir(PATH):
        true_filename = os.path.join(PATH,filename)
        if not os.path.isfile(true_filename):
            continue
        if not true_filename.endswith(".jsonl"):
            continue
        file = open(true_filename)
        graph_info = json.loads(file.readline())

        value = 0
        for line in file:
            value += 1
            config_info = json.loads(line)

            if not config_info["nef"]:
                continue
            if "type" in config_info:
                #QHD
                continue
            if config_info["K2"] not in K2:
                continue
            amount = config_info["#"]
            if amount == 1:
                # if "type" in config_info:
                #     print("QHD unimplemented")
                #     continue
                # else:
                body += single_chain(graph_info, config_info)
                body += f"\nExample taken from \\verb|{filename} : {value}|\n\n"

            else:
                p_extremal = config_info["WH"]
                if p_extremal == 0:
                    # if "type" in config_info:
                    #     print("QHD unimplemented")
                    # else:
                    body += double_chain(graph_info, config_info)
                    body += f"\nExample taken from \\verb|{filename} : {value}|\n\n"
                else:
                    body += double_chain(graph_info, config_info)
                    body += f"\nExample taken from \\verb|{filename} : {value}|\n\n"


    # body += "\\noindent\n$\\rule{12.5cm}{1.1pt}$\n"

    display_string(body)

if __name__ == "__main__":
    main()
