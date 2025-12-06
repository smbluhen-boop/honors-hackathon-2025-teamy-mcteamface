from drafter import *
from dataclasses import dataclass
from dataclasses import dataclass
import matplotlib.pyplot as plt


# hide_debug_information()
# set_website_framed(False)
set_website_title("Your Drafter Website")
set_site_information(
    "author",
    """
Your description can go here.
""",
    [],
    [],
    [],
)

@dataclass
class State:
    pass


@route
def index(state:State)->Page:
    '''
    Docstring for index
    
    :param state: Description
    :type state: State
    :return: Description
    :rtype: Any
    '''
    return Page(state,[
        "compare bear population to congres statistices!",
        Button("Let's start comparing!", data_combear)
    ])

@route
def data_combear(state:State)->Page:
    return Page(state,[
        "Choose the data you want to compare!!",
        Button("Bear population to senate seats", bear_to_senate_seats)
    ])

@route
def bear_to_senate_seats(state:State)->Page:
    bears=[]
    for line in open("bear_data_by_state"):
        parts=line.split("\t")
        state=parts[1]
        bear_pop=parts[2].strip()
        if bear_pop==-1:
            bear_pop=0
        else:
            bear_pop=int(bear_pop)
        bears.append((bear_pop))
    total_senate_seats_per_state=[]
    for index,line in enumerate(open("congress_data")):
        if index>0:
            parts=line.split()
            state=parts[0]
            total_senate_seats=int(parts[2])
            total_senate_seats_per_state.append((total_senate_seats))
    plt.scatter(x=bears,y=total_senate_seats_per_state),
    plt.xlabel("bear population"),
    plt.ylabel("congressional senate seats")
    plt.title("bears vs senate seats")
    plt.show()
    return Page(state, [
        MatPlotLibPlot(),
        Button("return to home", index)
    ])
    






start_server(State())
