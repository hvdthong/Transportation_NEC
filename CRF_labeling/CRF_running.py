__author__ = 'vdthoang'
from CRF_labeling.feature_crf_all import folder_files


if __name__ == '__main__':
    # loading CRF features
    path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'
    files_ = folder_files(path_ftr)

    for file in files_:
        print file
    print len(files_)
