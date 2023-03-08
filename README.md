# CISB-dataset
A dataset of Compiler-Introduced-Security-bugs (CISB) with reproduction materials.
These CISBs are manually collected from the GCC/Clang bugzilla and Linux kernel 
through an empirical study.

See our paper (to appear) for more information on the CISB taxonomy and collection methodology. 

Our data is stored in *CISB-dataset/dataset*.
More details [here](dataset/README.md).

# Reproduction Material

We provide the following reproduction materials:
- test code for all the reproducted CISB;
- an automatic tool to test whether one CISB is triggered with pre-defined oracles.

More details [here](reproduction_material/README.md)

# Aritifact setup
We provide a [Dockerfile](env/Dockerfile) that automates the setup process for our artifact.
With this Dockerfile, users can easily download the dataset and evaluation materials, as well as install all the necessary software requirements in one step.

For running one of the mitigation evaluation experiments that requires SPEC CPU 2006, it is recommended to mount the host directory containing SPEC CPU 2006 to a specific directory (/cisb_docker/CISB-dataset/spec/cpu2006) in the Docker container. Here are the instructions to build and run a Docker container with this:

1. Make sure you have Docker installed on your system.
2. Download the SPEC CPU 2006 benchmark and extract it to a directory on your host machine.
3. Navigate to the directory where you have the Dockerfile and run the following command to build the Docker image: 
```
cd path/to/Dockerfile
docker build -t cisb_docker .
```
It takes about 3 minutes to finish the build.

4. Once the build is complete, run the following command to start a container:
```
docker run -itd -v /path/to/cpu2006:/cisb_docker/CISB-dataset/spec/cpu2006 --name cisb_container --privileged cisb_docker
```

As an alternative, you can also place SPEC CPU 2006 anywhere you like within the Docker container. In that case, you will need to set the environment variable before running the experiment in the container.
```
export SEPC_CPU_2006_PATH='path/to/cpu2006'
``` 

5. Get into the Docker container:
```
docker exec -it cisb_container /bin/bash
```

6. Checkout to the stable commit for evaluation, which has been shown in the Artifact Appendix.
```
git checkout -b aaabbbccc
```

# Aritifact experiments
All of our experiments can be done through a [script](statistic.py).

## E1: CISB statistics

Execute the Python script to obtain the statistics of CISBs in our dataset. 
The result should be in line with the data in Figure 2 and Figure 3 of the paper.

```
python3 statistic.py -e cisb-statistics
```
## E2: Evaulation of mitigations
1. Review a list of bugs where the prevention performed by programmers failed. 
This list can be obtained by executing a script. The expected result is those CISBs exist.
```
python3 statistic.py -e human-mitigation
```
2. Run a script to obtain statistics on the effectiveness of compiler mitigations.
The output results should be in line with the data shown in Table 6 of the paper.
We also provide a [guide](compiler_strategies/README.md#effectiveness-evaluation) 
to measure the effectiveness of each strategy separately.
```
python3 statistic.py -e mitigation-effectiveness
```
3. Run two script to measure the overhead of different compiler prevention 
strategies using the SPEC CPU 2006 benchmark.
First, run the script to lauch all the SPEC CPU 2006 tests. It takes 40 hours
to finish all the tests. 
**You might need to [set up your SPEC CPU 2006](spec/README.md#setup-for-spec-cpu-2006) before that.**
```
python3 spec/config/test_all.py
```
Second, run a script to obtain the statistics of the overhead of tested mitigations 
```
python3 statistic.py -e mitigation-overhead
```
The output results should be in line with the data shown in Table 6 of the paper.
We also provide a [guide](spec/README.md#performance-evaluation-of-compiler-mitigations) 
to measure the overhead of each strategy separately.

<!-- As an alternative, you can also run the script to obtain all the results in one step.
```
python3 statistic.py -e mitigation-evaluation
``` -->

## E3: Target bugs of automatic prevention works
1. Execute the script to obtain the statistics of CISBs that can theoretically 
   be prevented by automatic prevention works. 
   The result should be in line with the data in Figure 7 of the paper.
```
python3 statistic.py -e target-cisb
```
2. Check the lists of CISBs we summarized and shown in the script. 
   These bugs should be within the scope of the corresponding prevention work.