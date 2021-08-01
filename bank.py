import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(42)
np.random.seed(42)

class Bank():

    def __init__(self, time, n_servers, branch_number):

        # Initialization
        self.time = time                 # full running time
        self.n_servers = n_servers       # number of servers
        self.branch_number = branch_number
        self.time_now = 0.0              # current system time(clock)
        self.m_total = 0                 # number of total customers
        self.FEL = list()                # FEL
        self.servers_state = {
            's'+str(i): 0 for i in range(1, n_servers+1)}      # servers state
        self.servers_service_time = {
            's'+str(i): 0 for i in range(1, n_servers+1)}                        # servers service time
        self.queue = 0                   # number of customers in queue
        # additionall helper variable to calculate waiting time
        self.queue_time = list()
        self.waited = 0
        self.waiting_time = 0.0          # waiting time
        self.waiting_time_total = 0.0    # total waiting time of system
        self.queue_cache = []
        self.time_cache = []

    def start_simulation(self):

        # first arrival event added to FEL
        self.FEL.append((0, self.generate_interarrival_time()))
        self.system_advance()

    def system_advance(self):
        '''
        This method works as system controller,
        and advances the system by checking the events of FEL
        '''
        while True:
            self.queue_cache.append(self.queue)
            self.time_cache.append(self.time_now)
            # checking nearest event in FEL
            min_event_time = 1e10
            for event_code, event_time in self.FEL:
                if event_time < min_event_time:
                    min_event_time = event_time
                    min_event_code = event_code

            # removing the nearest event from FEL
            self.FEL.remove((min_event_code, min_event_time))
            self.time_now = min_event_time

            # checking the system time
            if self.time_now < self.time:

                # checking event code and handlimg the corresponding event
                code = min_event_code
                if code == 0:
                    self.m_total += 1
                    a_star = self.generate_interarrival_time()  # adding next arrival event to FEL
                    self.FEL.append((0, self.time_now + a_star))

                    # assigning the arrived customer to a free server if there is one
                    if 0 in list((self.servers_state.values())):
                        servers_name_list = list(self.servers_state.keys())
                        states_list = list(self.servers_state.values())
                        temp = list(zip(servers_name_list, states_list))
                        random.shuffle(temp)
                        servers_name_list, states_list = zip(*temp)
                        free_server = servers_name_list[states_list.index(0)]
                        free_server_index = int(free_server[1:])
                        # setting server state to busy (1)
                        self.servers_state[free_server] = 1
                        # calculating random service time for new customer
                        service_time = self.generate_service_time()
                        # updating the server's service time
                        self.servers_service_time[free_server] += service_time
                        self.FEL.append(
                            (free_server_index, self.time_now+service_time))     # adding next departure event to FEL
                        continue

                    else:
                        # incrementing the queue in case all of the servers where busy
                        self.queue += 1
                        self.waited += 1
                        self.queue_time.append(self.time_now)
                        continue

                else:

                    server_index = code

                    if self.queue == 0:
                        # setting server state to free(0) if there was no one in the queue
                        self.servers_state['s'+str(server_index)] = 0
                        continue

                    else:
                        # getting the next person from the queue to be served
                        self.queue -= 1

                        # calculating the customer's waiting time
                        queued_time = self.queue_time.pop(0)
                        waiting_time = self.time_now - queued_time
                        self.waiting_time_total += waiting_time

                        # calculating random service time for new customer
                        service_time = self.generate_service_time()
                        # updating the server's service time
                        self.servers_service_time['s' +
                                                  str(server_index)] += service_time
                        # adding next departure event to FEL
                        self.FEL.append(
                            (server_index, self.time_now+service_time))
                        continue

            else:
                # calculating statistics and stoping simulation
                self.servers_engagement_percent = {
                    si: round((srv/self.time)*100) for si, srv in self.servers_service_time.items()}
                self.average_waiting_time = (
                    self.waiting_time_total/self.m_total)
                self.average_service_time = sum(list(
                    self.servers_service_time.values()))/len(list(self.servers_service_time.values()))
                self.stats = {'Total Number of Customers': self.m_total,
                              'Percentage of Servers Engagement': self.servers_engagement_percent,
                              'Average Waiting Time': self.average_waiting_time,
                              'Number of Costumers that Waited in Queue': self.waited,
                              'Average Service Time of Servers': self.average_service_time}
                #print('**************************\n* SIMULATION FINISHED ! *\n**************************')
                break

    def get_stats(self):
        return(self.stats)

    def generate_interarrival_time(self):
        '''
        This method generates random inter-arrival time
        '''
        return(np.random.uniform(2, 5))

    def generate_service_time(self):
        '''
        This method generates random service time
        '''
        return(abs(np.random.normal(10, 2)))