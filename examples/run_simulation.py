from pyfracman.run import FracmanRunner
import argparse
import pandas as pd

macro_filepath = 'tmp_macro.fmf'
input_file = 'input.in'

def run_simulation(macro_filepath):

    #PREPROCESS

    #RUN AND MONITOR
    fracman_runner = FracmanRunner()
    fracman_runner.Run(macro_filepath)

    #POSTPROCESS
    #read total trace length from f2d file and output
    with open('tracemap.f2d') as f:
        name = f.readline().split(maxsplit=2)[-1][:-1]
        cl = f.readline()[1:]
    columns = [s.strip() for s in cl.replace('\t', ' ').split(' ') if s]
    trace_data = pd.read_csv('tracemap.f2d', skiprows=2, index_col=False, sep='\s{2,}', names=columns, engine='python')

    total_length = trace_data['totlen[m]'].unique().sum()

    with open('trace_length.sts','w') as f:
        f.write(f'{total_length}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fracman macro runner')
    parser.add_argument('macro', type=str, nargs=1, help='FracMan macro filename')
    args = parser.parse_args()
    run_simulation(args.macro)
    