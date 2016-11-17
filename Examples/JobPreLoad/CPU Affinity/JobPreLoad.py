
def __main__( deadlinePlugin ):
    job = deadlinePlugin.GetJob()

    cpus = list(deadlinePlugin.CpuAffinity())

    cpus_linux = [str(x) for x in cpus]
    cpus_linux = ','.join(cpus_linux)

    # Edwin hex math for building the CPU affinity
    cpus_windows = 0
    for cpu in cpus:
        cpus_windows |= 1 << int(cpu)

    cpus_windows = hex(cpus_windows)[2:].upper()

    deadlinePlugin.LogInfo("Setting DEADLINE_CPUS_LINUX to {0}".format(cpus_linux))
    deadlinePlugin.SetProcessEnvironmentVariable("DEADLINE_CPUS_LINUX", cpus_linux)

    deadlinePlugin.LogInfo("Setting DEADLINE_CPUS_WINDOWS to {0}".format(cpus_windows))
    deadlinePlugin.SetProcessEnvironmentVariable("DEADLINE_CPUS_WINDOWS", cpus_windows)
