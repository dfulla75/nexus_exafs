
# Coments, bugs or improvements please contact Daniel Fulla 
# daniel.fulla.marsa@desy.de



import h5py
from matplotlib import pyplot as plt
import numpy as np
import sys
import os

class Read_hdf5(object):

    def __init__(self, file_to_read):
        
        self.file_to_read = file_to_read
    
    def object_assembler(self, path):

        data_file = h5py.File(self.file_to_read, "r")[path]        
        return data_file
    

    
    def make_file(self, file_to_read, scan, number, energy_list):
        
            file_basename = os.path.splitext(file_to_read)[0]
            file_data = open('%s_%s_%s.dat'%(file_basename,scan,number), 'w')  
                        
            for i, element in enumerate(energy_list):
            
                file_data.write('%f\t%f\n'%(element, edge_data[i]))

            file_data.close()
    

    def list_nexus(self):

        nexus_files = []
        for files in os.listdir('.'):
            
            if files.endswith(".nxs"):
                nexus_files.append(files)
        
        return nexus_files

    def make_plot(self, channel_data, data_energy, data_detector, scan):
        
        plt.subplot(121)
        plt.title('Max at channel:%i\nscan:%s'%(channel_max,str(scan)))
        plt.xlabel('Channel')
        plt.plot(data_channel[scan][:])                
            
        plt.subplot(122)
        plt.title('%s'%file_to_read)
        plt.xlabel('Energy [eV]')
        plt.plot(data_energy, data_detector[channel_max][:])
        
        plt.show()


if __name__ == '__main__':
    

    
    if len(sys.argv) != 4:
        
        nexus_files = Read_hdf5('').list_nexus()
        print nexus_files
        print sys.argv
        
        print 'ERROR: Please provide name of file followed by index and scan, \ne.g. python XANES_visualisation.py scan_00187.nxs 5 300'
    
    else:
    
        file_to_read = sys.argv[1]
        open_nexus = Read_hdf5(file_to_read)
    
        if not os.path.isfile(file_to_read):
            print 'ERROR: Cannot find the file. Check that the file is present in this directory'
            
        else:
    
            number = int(sys.argv[2])
            scan = int(sys.argv[3])
    
            path_data = ("/entry/instrument/collection/p06_xia0%i"%number)
            data_detector = np.array(open_nexus.object_assembler(path_data)).transpose()
    
            data_channel = (open_nexus.object_assembler(path_data))
            path_energy = '/entry/instrument/collection/energy_all'
            data_energy = open_nexus.object_assembler(path_energy)

            maximum = max(data_channel[scan][:])
            channel_max = np.argmax(data_channel[scan][:])
            
            edge_data = np.ndarray.tolist(data_detector[channel_max][:])
            energy_list = np.ndarray.tolist(np.array(data_energy))
            
            # make file with ascii data
            open_nexus.make_file(file_to_read, scan, number, energy_list)
            
            #plot channels and intensity vs energy
            open_nexus.make_plot(channel_max, data_energy, data_detector, scan )
            
            print 'Maximum: %.1f at channel: %i'%(maximum, channel_max)
    
