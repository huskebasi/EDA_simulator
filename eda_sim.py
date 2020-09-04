import numpy as np
import pandas as pd
import pry
import sys

class Simulation:
    def __init__(self): 
        self.clock=0.0                      #simulation clock
        self.num_arrivals=0                 #total number of arrivals
        self.t_arrival=self.gen_int_arr()   #time of next arrival
        self.t_departure1=float('inf')      #departure time from server 1
        self.t_departure2=float('inf')      #departure time from server 2
        self.dep_sum1=0                     #Sum of service times by teller 1
        self.dep_sum2=0                     #Sum of service times by teller 2
        self.server_state=0                 #current state of server1 (binary)
        self.total_wait_time=0.0            #total wait time
        self.num_in_q=0                     #current number in queue
        self.number_in_queue=0              #customers who had to wait in line(counter)
        self.num_of_departures1=0           #number of customers served by teller 1  
        self.num_of_departures2=0           #number of customers served by teller 2 
        self.lost_customers=0               #customers who left without service

        self.num_in_q=0
        self.num_in_system=0

    def time_adv(self):
        t_next_event=min(self.t_arrival,self.t_departure1)
        self.total_wait_time += (self.num_in_q*(t_next_event-self.clock))
        self.clock=t_next_event
                
        if self.t_arrival<self.t_departure1:
            self.arrival()
        else:
            self.teller1()

    def arrival(self):              
        self.num_arrivals += 1
        self.num_in_system += 1

        if self.num_in_q == 0:                                 #schedule next departure or arrival depending on state of servers
            if self.server_state==1:
                self.num_in_q+=1
                self.number_in_queue+=1
                self.t_arrival=self.clock+self.gen_int_arr()
            else: 
                self.server_state=1
                self.dep1= self.gen_service_time_teller1()
                self.dep_sum1 += self.dep1
                self.t_departure1=self.clock + self.dep1
                self.t_arrival=self.clock+self.gen_int_arr()

        else:
            self.num_in_q+=1
            self.number_in_queue+=1                             
            self.t_arrival=self.clock + self.gen_int_arr()

    def teller1(self):                #departure from server 2
        self.num_of_departures1 += 1
        if self.num_in_q>0:
            self.dep1= self.gen_service_time_teller1()
            self.dep_sum1 += self.dep1
            self.t_departure1=self.clock + self.dep1
            self.num_in_q-=1
        else:
            self.t_departure1=float('inf') 
            self.server_state=0


    def gen_int_arr(self):                                             #function to generate arrival times using inverse trasform
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 5)
    
    def gen_service_time_teller1(self):                                #function to generate service time for teller 1 using inverse trnasform
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 1.2)

# ---------------------------------------------------
# pry()
s = Simulation()
df = pd.DataFrame(columns=['Average interarrival time','Average service time teller1','Utilization teller 1','People who had to wait in line','Total average wait time','Lost Customers'])


for i in range(100):
    np.random.seed(i)
    s.__init__()
    while s.clock <= 240:
        s.time_adv()
        print(s.clock,  s.server_state, s.num_in_q)
    a=pd.Series([s.clock/s.num_arrivals, s.dep_sum1/s.num_of_departures1, s.dep_sum1/s.clock, s.number_in_queue,s.total_wait_time,s.lost_customers],index=df.columns)
    df=df.append(a,ignore_index=True)   
    
df.to_excel('results.xlsx')
