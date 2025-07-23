# Comparison script for fault injected taffo benchmarks

--- 
## installation requirements:
- [UV python package and project manager](https://docs.astral.sh/uv/)

This code was used to compare outputs from different fault injected variants of a single benchmark in the [taffo repository](https://github.com/TAFFO-org/TAFFO).
To use this code in taffo, the script in src/compare_results.py was copied over to the directory tests/polybench-cpu/, and run from the command line.
It is dependent on the existing structure of taffo. 


## Project setup instructions:
1. install python through uv:
`> uv python install 3.12`
2. create a virtual environment in the project: 
`> uv sync`
3. write your code and test it too!