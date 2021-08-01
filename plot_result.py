import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def plot_simulation_result(plot_data):


    branch_no_list = plot_data.get('branch_no')
    m_total_plot_data = plot_data.get('m_total')
    srvrs_engmnt_pct_plot_data = plot_data.get('srvrs_engmnt')
    avg_waiting_time_plot_data = plot_data.get('avg_waiting_time')
    num_of_waited_plot_data = plot_data.get('num_of_waited')
    avg_service_time_plot_data = plot_data.get('avg_service_time')
    last_branch_queue_cache = plot_data.get('last_branch_queue')
    last_branch_time_cache = plot_data.get('last_branch_time')
    n_servers = plot_data.get('n_servers')


    x = np.arange(len(branch_no_list))
    plt.style.use('tableau-colorblind10')
    plt.figure(figsize=(16, 12))
    plt.subplot(3, 2, 1)
    plt.bar(branch_no_list, m_total_plot_data)
    plt.title('Total Number of Customers', size=10)
    plt.ylabel('#', size=9)
    plt.xticks(size=7)
    plt.grid(axis='y')

    plt.subplot(3, 2, 2)
    plt.bar(branch_no_list, avg_waiting_time_plot_data)
    plt.title('Average Waithing Time', size=10)
    plt.ylabel('Time (minute)', size=8)
    plt.xticks(size=7)
    plt.grid(axis='y')

    plt.subplot(3, 2, 3)
    plt.bar(branch_no_list, num_of_waited_plot_data)
    plt.title('Number of Customers that Waited in Line', size=10)
    plt.ylabel('#', size=9)
    plt.xticks(size=7)
    plt.grid(axis='y')

    plt.subplot(3, 2, 4)
    plt.bar(branch_no_list, avg_service_time_plot_data)
    plt.title('Average Service Time of Servers', size=10)
    plt.ylabel('Time (minute)', size=8)
    plt.xticks(size=7)
    plt.grid(axis='y')

    if isinstance(n_servers, int):
        width = 0.4  # the width of the bars
        plt.subplot(3, 1, 3)
        for i in range(n_servers):
            plt.bar(x*5 + (-((n_servers-1)/2)+i)*width,
                    np.array(srvrs_engmnt_pct_plot_data).T[i], width)
        plt.ylabel('percent (%)', size=8)
        plt.title('Servers Engagement Percent', size=10)
        plt.xticks(x*5, branch_no_list, size=7)
        plt.grid(axis='y')
        plt.ylim((0, 100))
    else:
        lens = [len(i) for i in srvrs_engmnt_pct_plot_data]
        max_len = max(lens)
        for el in range(len(srvrs_engmnt_pct_plot_data)):
            srvrs_engmnt_pct_plot_data[el] = srvrs_engmnt_pct_plot_data[el] + [
                0 for _ in range(max_len - len(srvrs_engmnt_pct_plot_data[el]))]
        width = 0.4  # the width of the bars
        plt.subplot(3, 1, 3)

        for i in range(max(n_servers)):
            plt.bar(x*5 + (-((max(n_servers)-1)/2)+i)*width,
                    np.array(srvrs_engmnt_pct_plot_data).T[i], width)
        plt.ylabel('percent (%)', size=8)
        plt.title('Servers Engagement Percent', size=10)
        plt.xticks(x*5, branch_no_list, size=7)
        plt.grid(axis='y')
        plt.ylim((0, 100))

    plt.tight_layout(2)

    fig, ax = plt.subplots(1, 1)
    ax.step(last_branch_time_cache, last_branch_queue_cache)
    ax.grid()
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Number of customers in Line')
    ax.set_title('Queue Status')
    plt.show()