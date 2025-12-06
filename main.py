from drafter import *
from dataclasses import dataclass
from dataclasses import dataclass
import matplotlib.pyplot as plt

from meta import *

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
        Button("Let's start comparing!", "data_combear")
    ])

@route
def data_combear(state:State)->Page:
    return Page(state,[
        "Choose the data you want to compare!!",
        Button("Bear population to congressional seats",)
    ])

@route
def bear_to_seats(state:State)->Page:
    bears=[]
    for line in open("bear_data_by_state"):
        parts=line.split("\t")
        state=parts[1]
        bear_pop=parts[2].replace(",","").strip()
        if bear_pop==-1:
            bear_pop=0
        else:
            bear_pop=int(bear_pop)
        bears.append((bear_pop))
    total_seats_per_state=[]
    for index,line in enumerate(open("congress_data")):
        if index>0:
            parts=line.split(" ")
            state=parts[0]
            seats=int(parts[1].strip())
            total_seats_per_state.append((seats))
    






start_server(State())
