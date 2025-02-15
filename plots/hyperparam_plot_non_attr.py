import matplotlib.pyplot as plt
import numpy as np

# fix for type 3 fonts
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


# omit EColi for paper
class HyperTunerResults:
    M = [2, 5, 10, 20, 40]
    m = [2, 3, 5, 7]

    FORTY_PB = {
        "AUC": {

            (2, 40): np.array([94.11859, 94.28474, 94.23653, 95.03088, 94.76138]),
            (3, 40): np.array([94.07773, 93.92130, 94.10495, 94.92669, 94.84912]),
            (5, 40): np.array([93.66491, 93.69224, 94.09836, 94.99459, 94.71765]),
            (7, 40): np.array([93.51725, 93.44888, 93.89214, 94.54632, 94.36539]),
        },
        "Time": {
            (2, 40): np.array([354.85, 346.33, 355.40, 339.88, 341.98]),
            (3, 40): np.array([363.43, 377.71, 380.09, 379.95, 380.80]),
            (5, 40): np.array([458.56, 451.25, 445.56, 457.68, 467.25]),
            (7, 40): np.array([527.39, 534.95, 533.01, 540.11, 548.43]),
        }
    }

    RESULTS_NON = {
        'PB': {'AUC_MEAN': [86.945668, 91.9308, 93.505176, 94.19305, 88.125528, 92.15618, 93.876566, 94.22434000000001,
                            89.76083999999999, 92.71959, 93.891646, 94.09972200000001, 90.51021, 92.900018, 93.81096,
                            93.957076],
               'AP_MEAN': [87.190634, 91.518678, 93.158468, 93.84264600000002, 88.187284, 91.91599799999999, 93.553516,
                           93.927388, 89.77046599999998, 92.524974, 93.69295600000001, 93.86109400000001,
                           90.56883799999999, 92.80642, 93.61738, 93.855126],
               'Time_MEAN': [290.698, 294.626, 290.906, 309.61199999999997, 275.72400000000005, 285.98, 297.166,
                             316.832, 280.38, 296.38, 314.068, 354.9599999999999, 286.71999999999997, 304.926,
                             334.34000000000003, 394.342]},
        # 'Ecoli': {
        #     'AUC_MEAN': [92.348424, 95.381552, 96.081864, 96.192442, 93.24523599999999, 95.84468199999999, 96.43089,
        #                  96.46211000000001, 93.97460199999999, 95.785326, 96.30825, 96.34476, 94.19044799999999,
        #                  95.69772799999998, 95.98449, 96.18316],
        #     'AP_MEAN': [93.73167799999999, 96.26543799999999, 96.884578, 97.044354, 94.49142400000001,
        #                 96.64835000000002, 97.122936, 97.18846599999999, 95.175422, 96.6814, 97.03465, 97.151016,
        #                 95.417498, 96.70021, 96.947914, 97.073784],
        #     'Time_MEAN': [246.69800000000004, 243.28199999999998, 246.87800000000001, 257.756, 238.28199999999998,
        #                   246.208, 253.98600000000002, 271.98, 242.526, 255.08800000000002, 262.96400000000006,
        #                   305.126,
        #                   247.73000000000002, 260.618, 282.308, 361.218]}
    }

    SEAL = {
        'PB': {
            'AUC_MEAN': [94.43],
            'AP_MEAN': [94.07],
            'Time_MEAN': [896.0559999999999]},
        # 'Ecoli': {
        #     'AUC_MEAN': [96.67],
        #     'AP_MEAN': [97.38],
        #     'Time_MEAN': [907.384]
        # }
    }


if __name__ == '__main__':
    # multi-line graph plots for hyperparameter tuning results
    slice_length = len(HyperTunerResults.m)
    # colors = ['b', 'g', 'r', 'm', 'c', 'y', 'k', 'w']
    cmap = [plt.cm.get_cmap("Reds"), plt.cm.get_cmap("Greens")]
    slicedCM = [cmap[0](np.linspace(0.4, 0.75, slice_length)), cmap[1](np.linspace(0.5, 0.8, slice_length))]
    line_style = ['solid', 'dotted', 'dashed', 'dashdot']
    marker_style = ['D', 's', 'o', '^']
    seal_colors = ['midnightblue', 'darkgreen', ]

    for dataset, results in HyperTunerResults.RESULTS_NON.items():
        all_auc = results['AUC_MEAN']
        all_ap = results['AP_MEAN']
        all_times = results['Time_MEAN']

        time_SEAL_results = HyperTunerResults.SEAL[dataset]['Time_MEAN'] * 4

        auc_m_results = [all_auc[i:i + slice_length] for i in range(0, len(all_auc), slice_length)]
        time_m_results = [all_times[i:i + slice_length] for i in range(0, len(all_times), slice_length)]

        HyperTunerResults.RESULTS_NON[dataset].update(
            {'auc_m_results': auc_m_results, 'time_m_results': time_m_results}
        )

    f = plt.figure()
    x = HyperTunerResults.M
    default_x_ticks = range(len(x))
    plt.rcParams.update({'font.size': 16.5})
    plt.xticks(default_x_ticks, x)
    plt.yticks(np.arange(0, 96, 1))
    plt.ylim(84)
    for index, (dataset, results) in enumerate(HyperTunerResults.RESULTS_NON.items()):
        # SEAL line
        auc_SEAL_results = HyperTunerResults.SEAL[dataset]['AUC_MEAN'] * 5
        plt.plot(default_x_ticks, auc_SEAL_results, label=f"SEAL h=2", color=seal_colors[index],
                 linestyle='-', linewidth=2, markersize=10)

        for custom_index in range(len(HyperTunerResults.m)):
            auc_m_results = results['auc_m_results']
            mean_40 = np.mean(list(HyperTunerResults.FORTY_PB['AUC'].items())[custom_index][-1])
            auc_m_results[custom_index].append(mean_40)

        for inner_index, m_values in enumerate(auc_m_results):
            plt.plot(default_x_ticks, m_values, label=f"ScaLed h={HyperTunerResults.m[inner_index]}",
                     color=slicedCM[index][inner_index],
                     linestyle=line_style[inner_index], marker=marker_style[inner_index], linewidth=2, markersize=10)

    plt.ylabel('AUC Scores')
    plt.xlabel('k: Number of Walks')
    plt.legend(loc="lower right", ncol=2, borderpad=0.2, labelspacing=0.25, borderaxespad=0.25)
    plt.show()
    f.savefig("hypertuner_non_attr_auc.pdf", bbox_inches='tight')

    f = plt.figure()
    x = HyperTunerResults.M
    default_x_ticks = range(len(x))
    plt.rcParams.update({'font.size': 16.5})
    plt.xticks(default_x_ticks, x)
    plt.yticks(np.arange(0, 1050, 75))
    plt.ylim(0)
    for index, (dataset, results) in enumerate(HyperTunerResults.RESULTS_NON.items()):
        # SEAL line
        auc_SEAL_results = HyperTunerResults.SEAL[dataset]['Time_MEAN'] * 5
        plt.plot(default_x_ticks, auc_SEAL_results, label=f"SEAL h=2", color=seal_colors[index],
                 linestyle='-', linewidth=2, markersize=10)

        auc_m_results = results['time_m_results']
        for custom_index in range(len(HyperTunerResults.m)):
            auc_m_results = results['time_m_results']
            mean_40 = np.mean(list(HyperTunerResults.FORTY_PB['Time'].items())[custom_index][-1])
            auc_m_results[custom_index].append(mean_40)

        for inner_index, m_values in enumerate(auc_m_results):
            plt.plot(default_x_ticks, m_values, label=f"ScaLed h={HyperTunerResults.m[inner_index]}",
                     color=slicedCM[index][inner_index],
                     linestyle=line_style[inner_index], marker=marker_style[inner_index], linewidth=2, markersize=10)

    plt.ylabel('Runtime (sec)')
    plt.xlabel('k: Number of Walks')
    plt.legend(loc="lower right", ncol=2, borderpad=0.2, labelspacing=0.25, borderaxespad=0.25)
    plt.show()
    f.savefig("hypertuner_non_attr_time.pdf", bbox_inches='tight')
