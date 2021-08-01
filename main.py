import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from bank import Bank
from plot_result import plot_simulation_result


if __name__ == '__main__':

    time = 420
    n_servers = 5  # -> 'Integer' if 'same' for all branches otherwise 'list' or 'tuple' with different elements for each branch
    n_branches = 3
    iterations = 20
    t_statistic = 2.093  # p of 0.025 and 19 degrees of freedom

    if isinstance(n_servers, int):
        branch_stats = {}

        m_total_plot_data = []
        srvrs_engmnt_pct_plot_data = []
        avg_waiting_time_plot_data = []
        num_of_waited_plot_data = []
        avg_service_time_plot_data = []

        for branch_number in range(1, n_branches+1):

            m_total_list = []
            srvrs_engmnt_pct_list = []
            avg_waiting_time_list = []
            num_of_waited_list = []
            avg_service_time_list = []

            for _ in range(iterations):
                branch = Bank(time=time, n_servers=n_servers,
                              branch_number=branch_number)
                branch.start_simulation()

                srvrs_engmnt_pct_list.append(branch.servers_engagement_percent)
                m_total_list.append(branch.m_total)
                avg_waiting_time_list.append(branch.average_waiting_time)
                num_of_waited_list.append(branch.waited)
                avg_service_time_list.append(branch.average_service_time)

            srvrs_engmnt_pct = np.array(
                [np.array(list(a.values())) for a in srvrs_engmnt_pct_list])
            pt_est_eng_pct = {'server ' + str(i+1): '% '+str(round(srvrs_engmnt_pct.mean(
                axis=0)[i], 3)) for i in range(srvrs_engmnt_pct.mean(axis=0).shape[0])}
            interv_est_eng_pct = {
                'server ' + str(i+1): f'({round(srvrs_engmnt_pct.mean(axis=0)[i], 3) - t_statistic*round((srvrs_engmnt_pct.std(axis=0)[i]/(iterations**0.5)),3)} , {round(srvrs_engmnt_pct.mean(axis=0)[i], 3) + t_statistic*round((srvrs_engmnt_pct.std(axis=0)[i])/(iterations**0.5),3)})' for i in range(srvrs_engmnt_pct.mean(axis=0).shape[0])}
            m_total = np.array(m_total_list)
            avg_waiting_time = np.array(avg_waiting_time_list)
            num_of_waited = np.array(num_of_waited_list)
            avg_service_time = np.array(avg_service_time_list)

            m_total_plot_data.append(m_total.mean())
            srvrs_engmnt_pct_plot_data.append([round(srvrs_engmnt_pct.mean(
                axis=0)[i], 3) for i in range(srvrs_engmnt_pct.mean(axis=0).shape[0])])
            avg_waiting_time_plot_data.append(avg_waiting_time.mean())
            num_of_waited_plot_data.append(num_of_waited.mean())
            avg_service_time_plot_data.append(avg_service_time.mean())

            branch_stats['BRANCH '+str(branch_number)] = f'''
    Total Number of Customers:
        Point Estimation: {round(m_total.mean(),3)}
        Interval Estimation: ({round(m_total.mean() - t_statistic*(m_total.std()/(iterations**0.5)),3)} , {round(m_total.mean() + t_statistic*(m_total.std()/(iterations**0.5)),3)})
    
    Percentage of Servers Engagement':
        Point Estimation: {pt_est_eng_pct}
        Interval Estimation: {interv_est_eng_pct}

    Average Waiting Time:
        Point Estimation: {round(avg_waiting_time.mean(),3)}
        Interval Estimation: ({round(avg_waiting_time.mean() - t_statistic*(avg_waiting_time.std()/(iterations**0.5)),3)} , {round(avg_waiting_time.mean() + t_statistic*(avg_waiting_time.std()/(iterations**0.5)),3)})
    
    Number of Costumers that Waited in Queue:
        Point Estimation: {round(num_of_waited.mean(),3)}
        Interval Estimation: ({round(num_of_waited.mean() - t_statistic*(num_of_waited.std()/(iterations**0.5)),3)} , {round(num_of_waited.mean() + t_statistic*(num_of_waited.std()/(iterations**0.5)),3)})
    
    Average Service Time of Servers:
        Point Estimation: {round(avg_service_time.mean(),3)}
        Interval Estimation: ({round(avg_service_time.mean() - t_statistic*(avg_service_time.std()/(iterations**0.5)),3)} , {round(avg_service_time.mean() + t_statistic*(avg_service_time.std()/(iterations**0.5)),3)})
        '''
        last_branch_queue_cache = branch.queue_cache
        last_branch_time_cache = branch.time_cache

    elif isinstance(n_servers, tuple) or isinstance(n_servers, list):
        if len(n_servers) != n_branches:
            raise Exception(
                'number of servers does not match number of branches!')
        else:
            branch_stats = {}

            m_total_plot_data = []
            srvrs_engmnt_pct_plot_data = []
            avg_waiting_time_plot_data = []
            num_of_waited_plot_data = []
            avg_service_time_plot_data = []

            for branch_number in range(1, n_branches+1):

                m_total_list = []
                srvrs_engmnt_pct_list = []
                avg_waiting_time_list = []
                num_of_waited_list = []
                avg_service_time_list = []

                for _ in range(iterations):
                    branch = Bank(
                        time=time, n_servers=n_servers[branch_number-1], branch_number=branch_number)
                    branch.start_simulation()

                    srvrs_engmnt_pct_list.append(
                        branch.servers_engagement_percent)
                    m_total_list.append(branch.m_total)
                    avg_waiting_time_list.append(branch.average_waiting_time)
                    num_of_waited_list.append(branch.waited)
                    avg_service_time_list.append(branch.average_service_time)

                srvrs_engmnt_pct = np.array(
                    [np.array(list(a.values())) for a in srvrs_engmnt_pct_list])
                pt_est_eng_pct = {'server ' + str(i+1): '% '+str(round(srvrs_engmnt_pct.mean(
                    axis=0)[i], 3)) for i in range(srvrs_engmnt_pct.mean(axis=0).shape[0])}
                interv_est_eng_pct = {
                    'server ' + str(i+1): f'({round(srvrs_engmnt_pct.mean(axis=0)[i], 3) - t_statistic*round(srvrs_engmnt_pct.std(axis=0)[i],3)} , {round(srvrs_engmnt_pct.mean(axis=0)[i], 3) + t_statistic*round(srvrs_engmnt_pct.std(axis=0)[i],3)})' for i in range(srvrs_engmnt_pct.mean(axis=0).shape[0])}
                m_total = np.array(m_total_list)
                avg_waiting_time = np.array(avg_waiting_time_list)
                num_of_waited = np.array(num_of_waited_list)
                avg_service_time = np.array(avg_service_time_list)

                m_total_plot_data.append(m_total.mean())
                srvrs_engmnt_pct_plot_data.append([round(srvrs_engmnt_pct.mean(
                    axis=0)[i], 3) for i in range(srvrs_engmnt_pct.mean(axis=0).shape[0])])
                avg_waiting_time_plot_data.append(avg_waiting_time.mean())
                num_of_waited_plot_data.append(num_of_waited.mean())
                avg_service_time_plot_data.append(avg_service_time.mean())

                branch_stats['BRANCH '+str(branch_number)] = f'''
    Total Number of Customers:
        Point Estimation: {round(m_total.mean(),3)}
        Interval Estimation: ({round(m_total.mean() - t_statistic*(m_total.std()/(iterations**0.5)),3)} , {round(m_total.mean() + t_statistic*(m_total.std()/(iterations**0.5)),3)})
    
    Percentage of Servers Engagement':
        Point Estimation: {pt_est_eng_pct}
        Interval Estimation: {interv_est_eng_pct}

    Average Waiting Time:
        Point Estimation: {round(avg_waiting_time.mean(),3)}
        Interval Estimation: ({round(avg_waiting_time.mean() - t_statistic*(avg_waiting_time.std()/(iterations**0.5)),3)} , {round(avg_waiting_time.mean() + t_statistic*(avg_waiting_time.std()/(iterations**0.5)),3)})
    
    Number of Costumers that Waited in Queue:
        Point Estimation: {round(num_of_waited.mean(),3)}
        Interval Estimation: ({round(num_of_waited.mean() - t_statistic*(num_of_waited.std()/(iterations**0.5)),3)} , {round(num_of_waited.mean() + t_statistic*(num_of_waited.std()/(iterations**0.5)),3)})
    
    Average Service Time of Servers:
        Point Estimation: {round(avg_service_time.mean(),3)}
        Interval Estimation: ({round(avg_service_time.mean() - t_statistic*(avg_service_time.std()/(iterations**0.5)),3)} , {round(avg_service_time.mean() + t_statistic*(avg_service_time.std()/(iterations**0.5)),3)})
        '''

            last_branch_queue_cache = branch.queue_cache
            last_branch_time_cache = branch.time_cache

    for branch_no, stats in branch_stats.items():
        print(branch_no+': ')
        print(stats)
        print('--------------------------------')

    branch_no_list = ['BRANCH '+str(i+1) for i in range(n_branches)]

    plot_data = {
                'n_servers': n_servers,
                'branch_no' : branch_no_list,
                'm_total' : m_total_plot_data,
                'srvrs_engmnt' : srvrs_engmnt_pct_plot_data,
                'avg_waiting_time' : avg_waiting_time_plot_data,
                'num_of_waited' : num_of_waited_plot_data,
                'avg_service_time' : avg_service_time_plot_data,
                'last_branch_queue' : last_branch_queue_cache,               
                'last_branch_time' : last_branch_time_cache
    }

    plot_simulation_result(plot_data)