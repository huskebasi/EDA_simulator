import numpy as np
import pandas as pd
import pry
import sys

class Simulation:
    def __init__(self):
        self.rho=0.5                        #Thinning probability
        self.ETBA=5                         #Expected Time Between Arrival

        self.clock=0.0                      #simulation clock
        self.num_arrivals=0                 #total number of arrivals
        self.t_arrival=self.gen_int_arr()   #time of next arrival
        self.t_landing=float('inf')         #landing time from server
        self.land_sum=0                      #Sum of landing times
        self.server_state=0                 #current state of server (binary)
        self.total_wait_time=0.0            #total wait time
        self.num_in_q=0                     #current number in queue
        self.tot_in_queue=0                 #planes who had to wait in line

    def time_adv(self):
        t_next_event=min(self.t_arrival,self.t_landing)
        self.total_wait_time += (self.num_in_q*(t_next_event-self.clock))
        self.clock=t_next_event

        if self.t_arrival<self.t_landing:
            self.arrival()
        else:
            self.landing()
        print()

    def arrival(self):              
        self.num_arrivals += 1
        self.tot_in_queue += 1

        if self.num_in_q == 0:                                 #schedule next departure or arrival depending on state of servers
            if self.server_state==1:
                self.num_in_q+=1
                self.tot_in_queue+=1
            else: 
                self.server_state=1
                self.land= self.gen_landing_time()
                self.land_sum += self.land
                self.t_landing=self.clock + self.land
        else:
            self.num_in_q+=1
            self.tot_in_queue+=1                   

        self.t_arrival=self.clock + self.gen_int_arr()  # generate next arrival time

    def landing(self):
        if self.num_in_q>0:
            self.land= self.gen_landing_time()
            self.land_sum += self.land
            self.t_landing=self.clock + self.land
            self.num_in_q-=1
        else:
            self.t_landing=float('inf') 
            self.server_state=0


    def gen_int_arr(self):
        # return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 5)  # exponential arrivals
        if np.random.uniform() < self.rho:
        	self.clock += np.random.uniform()*self.ETBA
        return np.random.uniform()*self.ETBA
    
    def gen_landing_time(self):
        # return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 1.2)   # exponential service time
        return 1  # deterministic service time

# ---------------------------------------------------

s = Simulation()
df = pd.DataFrame(columns=['Average interarrival time','Utilization track','Planes who had to wait in line','Total average wait time'])


for i in range(1):
    np.random.seed(i)
    # pry()
    s.__init__()
    while s.clock <= 24:
        print(s.clock,  s.server_state, s.num_in_q, end =" ")
        s.time_adv()
    a=pd.Series([s.clock/s.num_arrivals, s.land_sum/s.clock, s.tot_in_queue,s.total_wait_time],index=df.columns)
    df=df.append(a,ignore_index=True)   
    
df.to_excel('results.xlsx')
