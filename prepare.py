import os
import shutil
import json
from utils.rep2graph import Rep2Graph
import glob



class PrepareData():

    #? under each dir_data_..., data must be grouped by label (eg. each data dir contains 2 folder: benign & malware, under which contains files)
    dir_data_report = 'data/reports/TuTu_sm' #? directory that contains cuckoo reports by labels
    dir_data_json = 'data/json/TuTu_sm'
    dir_data_graph = 'data/graphs/TuTu_sm' #? store encoded graph for training / testing
    dir_data_graphviz = 'data/graphviz/TuTu_sm' #? store dot file for visualization
    dir_data_networkx = 'data/nx/TuTu_sm' #? store visualization of networkx graph (img)
    dir_data_pickle = 'data/pickle/TuTu_sm'
    dir_data_embedding = 'data/embeddings/TuTu_sm'

    mapping_labels = {'benign': 0, 'malware': 1}


    def __init__(self, config_filepath='config.prepare.json') -> None:
        """ Load config """
        if not os.path.isfile(config_filepath):
            print(f'[x] config file not exist')
            exit()
        
        self.__config__ = json.load(open(config_filepath))

        self.obj_r2g = Rep2Graph(self.__config__)

        pass


    def from_set(self) -> None:
        """
        Process a set of reports.
        Folder of a set must divide into n subfolders (n = num classes)
        """
        self.dir_data_report = self.__config__['dir_data_report']
        self.dir_data_report_cut = self.__config__['dir_data_report_cut']
        self.dir_data_json = self.__config__['dir_data_json']
        self.dir_data_graph = self.__config__['dir_data_graph']
        self.dir_data_graphviz = self.__config__['dir_data_graphviz']
        self.dir_data_networkx = self.__config__['dir_data_networkx']
        self.dir_data_pickle = self.__config__['dir_data_pickle']
        self.dir_log = self.__config__['dir_log']


        """ Create data dir if not exist """
        for dir in [self.dir_data_embedding, self.dir_data_report, self.dir_data_report_cut, self.dir_data_json, self.dir_data_pickle, self.dir_data_graph, self.dir_data_graphviz, self.dir_data_networkx, self.dir_log]:
            print(f'[ ] Checking dir {dir}')
            if not os.path.isdir(dir):
                print(f'[!] Not exist. Creating {dir}')
                os.makedirs(dir)
        #? these data dir has sub folders which represent classes (labels)
        for dir in [self.dir_data_report, self.dir_data_report_cut, self.dir_data_json, self.dir_data_graph, self.dir_data_graphviz, self.dir_data_networkx, self.dir_log]:
            for lbl in self.mapping_labels.keys():
                dir_data_smt_by_lbl = os.path.join(dir, lbl)
                if not os.path.isdir(dir_data_smt_by_lbl):
                    os.makedirs(dir_data_smt_by_lbl)


        """ Process each label dir """
        for lbl in self.mapping_labels.keys():
            #? create output
            n = 0

            #? Get a list of files (file paths) in the given directory 
            report_file_paths = filter(os.path.isfile, glob.glob(os.path.join(self.dir_data_report, lbl, '*')))
            #? Sort list of files in directory by size 
            report_file_paths = sorted(report_file_paths, key = lambda x: os.stat(x).st_size)
            # print('>> report_file_paths', report_file_paths)

            doBreak = False
            doSkip = True

            pfname = os.path.join('data', f'processed.{lbl}.txt')
            processedList = [line.strip() for line in open(pfname, 'r').readlines()] if os.path.isfile(pfname) else []
            print('processedList', processedList)

            for report_file_path in report_file_paths:
                #! DEBUG
                # if '9bb89bbdc1c0a2bd3c36533074c9972f80f4a7952c9b85c6d57b2023f1a4f921__5168.json' not in report_file_path:
                #     continue
                # if '0b85c7c1ec8fcda37d6b3cdc21eda44d2ba4b7814e09b16a5a8e05df493ebdc2__VirusShare_b63a9c0976f82e7e19b512f3b9eb9f1f__4304' not in report_file_path:
                #     continue

                filename = os.path.basename(report_file_path)

                if not os.path.isfile(report_file_path):
                    print(f'[x] Not exist. Skip')
                    continue

                # if doSkip is True:
                #     if report_file_path in processedList:
                #         print('[!] Processed. Skip.')
                #         continue
                #     elif os.path.exists(os.path.join(self.dir_data_networkx, filename+'.svg')):
                #         print('[!] Processed. Skip.')
                #         open(pfname, 'a').write(f'\n{report_file_path}')
                #         continue


                # print(f'self.dir_data_graphviz: {self.dir_data_graphviz}')
                # self.dir_data_networkx = None
                dir_out_report_cut = os.path.join(self.dir_data_report_cut, lbl)
                dir_out_nx = os.path.join(self.dir_data_networkx, lbl)
                dir_out_graphviz = os.path.join(self.dir_data_graphviz, lbl)
                dir_out_log = os.path.join(self.dir_log, lbl)
                stt = self.obj_r2g.r2g(report_file_path, lbl, dir_out_log, dir_out_report_cut, dir_out_nx, dir_out_graphviz, render_svg=True)
                
                print(f'\n[+] r2g return {stt}')

                processedList.append(report_file_path)
                open(pfname, 'a').write(f'\n{report_file_path}')
                
                n += 1

                if doBreak is True and n > 0:
                    break



if __name__ == '__main__':
    preparer = PrepareData()
    preparer.from_set()