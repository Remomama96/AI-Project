import streamlit as st
import altair as alt
import pandas as pd, seaborn as sns,numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import random
import pickle



html_temp = """ 
    <div style ="background-color:grey;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Vacation Planner </h1> 
    </div> 
    """

st.markdown(html_temp, unsafe_allow_html = True) 
    
 
Budget = int(st.number_input('Insert vacation budget', min_value=100, step=1, value=5000))
    
Vac_Dur = int(st.number_input('Insert vacation duration', min_value=1, step=1, value=5))

Gen = int(st.number_input('Insert number of generations', min_value=1, step=1, value=100))    
Population_size = int(st.number_input('Insert population size', min_value=1, step=1, value=10))



  
def individual():
    Hotel = random.randint(100,500)
    Tourist_spot= random.randint(2, 10)
    Tourist_spot_cost = random.randint(5, 300)
    Food = random.randint(10, 100)
    Transport_cost = random.randint(5, 100)
    Transport_freq = random.randint(1,10)
     
    return [Hotel,Tourist_spot,Tourist_spot_cost,Food,Transport_cost,Transport_freq] 

def generate_population(size):
        population = []
        for i in range(size):
            population.append(individual())
        
        return population

    #Fitness score LOWER IS BETTER
def fitness(individual):
    # [hotel,food_per_meals,t_spots,one_t_spots,t_fee,t_fre]
    total = individual[0]*4 + individual[1]*3*Vac_Dur + individual[2]*individual[3] + individual[4]*individual[5]*Vac_Dur
    return abs(Budget - total)

def grade(pop):
        total = 0
        for p in pop:
            f = fitness(p)
            total += f
            
        return total / len(pop)
                
def evolve(pop, retain, crossover1, crossover2, mutate, random_select = 0.05): #rank selection, random mutation, single point crossover
        graded = [(fitness(x),x) for x in pop]
        graded = [x[1] for x in sorted(graded)]
        retain_length = int(len(graded)*retain)
        parents = graded[0:retain_length]

        for individual in graded[retain_length:]:
            if random_select > random.random():
                parents.append(individual)

        for individual in parents:
            if mutate > random.random():
                pos_to_mutate = random.randint(0,len(individual)-1)
                individual[pos_to_mutate] = random.randint(min(individual),max(individual))
        
        #crossover parents to create children
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []
        while len(children) < desired_length:
            male = random.randint(0,parents_length) - 1
            female = random.randint(0,parents_length) - 1
            if male != female:
                male = parents[male]
                female = parents[female]
                half = int(len(male)/2)
                child = male[:crossover1] + female[crossover2:]
                children.append(child)
                
        parents.extend(children)
        return parents

    
def gen():
    # Result
    # Decalaration of list
    value_lst =[]
    fitness_history = []

    p = generate_population(Population_size)

    # Iterate and modeling for result
    for i in range(Gen):
        p = evolve(p, retain, crossover1, crossover2, mutate)
        value = grade(p)
        fitness_history.append(value)
        value_lst.append(p[0])
        value_lst.append(value)

    

    best_model = value_lst[-2]
    best_fit = value_lst[-1]


    
    
    st.write("Vacation Budget      = RM",Budget)
    st.write("Vacation duration   =",Vac_Dur,"days")
    st.write("Hotel Price         = RM", best_model[0])
    st.write("Food Price          = RM", best_model[1],"per meal")
    st.write("Travel Spot         =",best_model[2],"spots")
    st.write("One Spot Price      = RM", best_model[3])
    st.write("Transport Fee       = RM", best_model[4])
    st.write("Transport Frequency =", best_model[5],"trip per day")
    total = best_model[0]*4 + best_model[1]*3*Vac_Dur + best_model[2]*best_model[3] + best_model[4]*best_model[5]*Vac_Dur
    st.write("Total expenses: RM", total)

    df_hist = pd.DataFrame()
    df_hist["Generation"] = [x + 1 for x in list(range(len(fitness_history)))]
    df_hist["Fitness History"] = fitness_history

    return fitness_history, best_fit, df_hist


cols = st.columns(3)
with cols[0]:
    st.write("**First Option**")
    retain = 0.1
    mutate = 0.01
    crossover1 = 1
    crossover2 = 1
    st.write(" ")
    hist1, fit1, df1 = gen()
    st.markdown("""---""")
    
with cols[1]:
    st.write("**Second Option**")
    retain = 0.2
    mutate = 0.02
    crossover1 = 2
    crossover2 = 2
    st.write(" ")
    hist2, fit2, df2 = gen()
    st.markdown("""---""")

with cols[2]:
    st.write("**Third Option**")
    retain = 0.3
    mutate = 0.03
    crossover1 = 3
    crossover2 = 3
    st.write(" ")
    hist3, fit3, df3 = gen()
    st.markdown("""---""")



