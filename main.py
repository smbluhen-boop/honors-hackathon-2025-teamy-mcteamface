
from drafter import *
from dataclasses import dataclass
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np


hide_debug_information()
set_website_framed(False)
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
    bear_width:int
    bear_length:int
    bears:list[int]


@route
def index(state:State)->Page:
    '''
    Docstring for index
    
    :param state: Description
    :type state: State
    :return: Description
    :rtype: Any
    '''
    state.bears=[]
    bears=[]
    for line in open("bear_data_by_state"):
        parts=line.split("\t")
        bear_pop=parts[2].strip()
        if bear_pop==-1:
            bear_pop=0
        else:
            bear_pop=int(bear_pop)
        bears.append((int(bear_pop)))
    state.bears=bears
    return Page(state,[
        Image("fat_bear_1.jpg", state.bear_width, state.bear_length),
        Button("Fatten Bear", "fatten_bear"),
        "Compare bear population to state congress statistics!",
        Button("Let's start comparing!", data_combear),
        Button("Bear population for each state", "get_state_list")
    ])

@route
def fatten_bear (state: State) -> Page:
    state.bear_width = state.bear_width + 10
    return index(state)

@route
def get_state_list (state: State) -> Page:
    minibears = []
    states = []
    for line in open("bear_data_by_state"):
        parts=line.split("\t")
        location=parts[1]
        states.append(location)
        bear_pop=parts[2].replace(",","").strip()
        if bear_pop==-1:
            bear_pop=0
        else:
            bear_pop=int(bear_pop)
        minibears.append((str(bear_pop)))
    return Page(state, [
        'If the bear population is "-1", then there is no recorded population of black bears.',
        Table([states,minibears]),
        Button("Return to Main Page", "index")
        ])

@route
def data_combear(state:State)->Page:
    return Page(state,[
        "Choose the data you want to compare!!",
        Button("Bear population to senate seats", bear_to_senate_seats),
        LineBreak(),
        Button("Bear population to house seats", bear_to_house_seats),
        LineBreak(),
        Button("Bear population to senate party composition", party_composition_compare_senate),
        LineBreak(),
        Button("Bear population to house party composition", party_composition_compare_house)
    ])

@route
def bear_to_senate_seats(state:State)->Page:
    total_senate_seats_per_state=[]
    for i,line in enumerate(open("congress_data")):
        if i>0:
            parts=line.split()
            location=parts[0]
            total_senate_seats=int(parts[2])
            total_senate_seats_per_state.append((total_senate_seats))
    filt_bears=[]
    filt_senate=[]
    for i,bear in enumerate(state.bears):
         if not (bear==0 or bear ==-1):
            filt_bears.append(bear)
            filt_senate.append(total_senate_seats_per_state[i])
    x=np.array(filt_bears)
    y=np.array(filt_senate)

    slope, y_int=np.polyfit(x,y,1)
    trendline=slope*x+y_int
    plt.plot(x,trendline,color='Blue',label='trendline')
    plt.scatter(x,y),
    plt.xlabel("bear population"),
    plt.ylabel("state senate seats")
    plt.title("bears vs senate seats")
    plt.show()
    return Page(state, [
        MatPlotLibPlot(),
        Button("return to home", index)
    ])
    
@route
def bear_to_house_seats(state:State)->Page:
    total_house_seats_per_state=[]
    for i,line in enumerate(open("congress_data")):
        if i>0:
            parts=line.split()
            location=parts[0]
            if not location=="Nebraska":
                    total_house_seats=int(parts[5])
                    total_house_seats_per_state.append((total_house_seats))
            else:
                total_house_seats_per_state.append(0)
    filt_bears=[]
    filt_house=[]
    for i,bear in enumerate(state.bears):
         if not (bear==0 or bear ==-1):
            filt_bears.append(bear)
            filt_house.append(total_house_seats_per_state[i])
    x=np.array(filt_bears)
    y=np.array(filt_house)
    slope, y_int=np.polyfit(x,y,1)
    trendline=slope*x+y_int
    plt.plot(x,trendline,color='Blue',label='trendline')
    plt.scatter(x,y),
    plt.xlabel("bear population"),
    plt.ylabel("state house seats")
    plt.title("bears vs house seats")
    plt.show()
    return Page(state, [
        MatPlotLibPlot(),
        Button("return to home", index)
    ])

@route
def party_composition_compare_senate(state:State)->Page:
    dem_percents=[]
    rep_percents=[]
    for i,line in enumerate(open("congress_data")):
        if i>0:
            parts=line.split()
            location=parts[0]
            if not location=="Nebraska":
                    dem_percents.append(int(parts[3])/(int(parts[2]))*100)
                    rep_percents.append(int(parts[4])/(int(parts[2]))*100)
            else:
                dem_percents.append(0)
                rep_percents.append(0)
    filt_bears=[]
    for i,bear in enumerate(state.bears):
         if not (bear==0 or bear==-1):
            filt_bears.append(bear)
            dem_percents.append(dem_percents[i])
            rep_percents.append(rep_percents[i])
    x=np.array(filt_bears)
    dem_percents=dem_percents[50:]
    rep_percents=rep_percents[50:]
    dem_y=np.array(dem_percents)
    rep_y=np.array(rep_percents)
    dem_slope, dem_y_int=np.polyfit(x,dem_y,1)
    rep_slope, rep_y_int=np.polyfit(x,rep_y,1)
    dem_trendline=dem_slope*x+dem_y_int
    rep_trendline=rep_slope*x+rep_y_int
    plt.scatter(x=filt_bears,y=dem_percents,color='blue',label='democrat percentage')
    plt.plot(x,dem_trendline,color='cyan',label='democrat trendline')
    plt.plot(x,rep_trendline,color='orange',label='republican trendline')
    plt.scatter(x=filt_bears,y=rep_percents,color='red',label='republican percentage')
    plt.xlabel("bear population")
    plt.ylabel("percentage in state senate")
    plt.title("bears vs percentage held in senate")
    plt.show()
    return Page(state, [
        MatPlotLibPlot(),
        Button("return to home", index)
    ])

@route
def party_composition_compare_house(state:State)->Page:
    dem_percents=[]
    rep_percents=[]
    for i,line in enumerate(open("congress_data")):
        if i>0:
            parts=line.split()
            location=parts[0]
            if not location=="Nebraska":
                    dem_percents.append(int(parts[6])/(int(parts[5]))*100)
                    rep_percents.append(int(parts[7])/(int(parts[5]))*100)
            else:
                dem_percents.append(0)
                rep_percents.append(0)
    filt_bears=[]
    for i,bear in enumerate(state.bears):
         if not (bear==0 or bear ==-1):
            filt_bears.append(bear)
            dem_percents.append(dem_percents[i])
            rep_percents.append(rep_percents[i])
    x=np.array(filt_bears)
    dem_percents=dem_percents[50:]
    rep_percents=rep_percents[50:]
    dem_y=np.array(dem_percents)
    rep_y=np.array(rep_percents)
    dem_slope, dem_y_int=np.polyfit(x,dem_y,1)
    rep_slope, rep_y_int=np.polyfit(x,rep_y,1)
    dem_trendline=dem_slope*x+dem_y_int
    rep_trendline=rep_slope*x+rep_y_int
    plt.scatter(x=filt_bears,y=dem_percents,color='blue',label='democrat percentage')
    plt.plot(x,dem_trendline,color='cyan',label='democrat trendline')
    plt.plot(x,rep_trendline,color='orange',label='republican trendline')
    plt.scatter(x=filt_bears,y=rep_percents,color='red',label='republican percentage')
    plt.xlabel("bear population")
    plt.ylabel("percentage in state house")
    plt.title("bears vs percentage held in house")
    plt.show()
    return Page(state, [
        MatPlotLibPlot(),
        Button("return to home", index)
    ])




start_server(State(100,100,[]))
