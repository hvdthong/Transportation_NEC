__author__ = 'vdthoang'
from nec_demo.filterText_demo import load_sql, table_SQL, filtering_text_demo
from multiprocessing import Pool, Process
from CRF_labeling.feature_crf import match_road_busstop
from main.writeFile import write_file


def running_road(command):
    if command == 'twitter':
        pr1 = Process(target=match_road_busstop, args=(list_line_[0:21006], 'road', 1))
        pr2 = Process(target=match_road_busstop, args=(list_line_[21006:42003], 'road', 2))
        pr3 = Process(target=match_road_busstop, args=(list_line_[42003:63000], 'road', 3))
        pr4 = Process(target=match_road_busstop, args=(list_line_[63000:84006], 'road', 4))
        pr5 = Process(target=match_road_busstop, args=(list_line_[84006:105003], 'road', 5))
        pr6 = Process(target=match_road_busstop, args=(list_line_[105003:126000], 'road', 6))
        pr7 = Process(target=match_road_busstop, args=(list_line_[126000:147006], 'road', 7))
        pr8 = Process(target=match_road_busstop, args=(list_line_[147006:168003], 'road', 8))
        pr9 = Process(target=match_road_busstop, args=(list_line_[168003:189000], 'road', 9))
        pr10 = Process(target=match_road_busstop, args=(list_line_[189000:210006], 'road', 10))
        pr11 = Process(target=match_road_busstop, args=(list_line_[210006:], 'road', 11))

        pr1.start(), pr2.start(), pr3.start(), pr4.start(), pr5.start()
        pr6.start(), pr7.start(), pr8.start(), pr9.start(), pr10.start(), pr11.start()

        pr1.join(), pr2.join(), pr3.join(), pr4.join(), pr5.join()
        pr6.join(), pr7.join(), pr8.join(), pr9.join(), pr10.join(), pr11.join()

    elif command == 'sgforums':
        pr1 = Process(target=match_road_busstop, args=(list_line_[0:3000], 'road', 1))
        pr2 = Process(target=match_road_busstop, args=(list_line_[3000:6000], 'road', 2))
        pr3 = Process(target=match_road_busstop, args=(list_line_[6000:9000], 'road', 3))
        pr4 = Process(target=match_road_busstop, args=(list_line_[9000:12000], 'road', 4))
        pr5 = Process(target=match_road_busstop, args=(list_line_[12000:15000], 'road', 5))
        pr6 = Process(target=match_road_busstop, args=(list_line_[15000:18000], 'road', 6))
        pr7 = Process(target=match_road_busstop, args=(list_line_[18000:21000], 'road', 7))
        pr8 = Process(target=match_road_busstop, args=(list_line_[21000:24000], 'road', 8))
        pr9 = Process(target=match_road_busstop, args=(list_line_[24000:27000], 'road', 9))
        pr10 = Process(target=match_road_busstop, args=(list_line_[27000:30000], 'road', 10))
        pr11 = Process(target=match_road_busstop, args=(list_line_[30000:], 'road', 11))

        pr1.start(), pr2.start(), pr3.start(), pr4.start(), pr5.start()
        pr6.start(), pr7.start(), pr8.start(), pr9.start(), pr10.start(), pr11.start()

        pr1.join(), pr2.join(), pr3.join(), pr4.join(), pr5.join()
        pr6.join(), pr7.join(), pr8.join(), pr9.join(), pr10.join(), pr11.join()

    elif command == 'facebook':
        pr1 = Process(target=match_road_busstop, args=(list_line_[0:9000], 'road', 1, command))
        pr2 = Process(target=match_road_busstop, args=(list_line_[9000:18000], 'road', 2, command))
        pr3 = Process(target=match_road_busstop, args=(list_line_[18000:27000], 'road', 3, command))
        pr4 = Process(target=match_road_busstop, args=(list_line_[27000:36000], 'road', 4, command))
        pr5 = Process(target=match_road_busstop, args=(list_line_[36000:45000], 'road', 5, command))
        pr6 = Process(target=match_road_busstop, args=(list_line_[45000:54000], 'road', 6, command))
        pr7 = Process(target=match_road_busstop, args=(list_line_[54000:63000], 'road', 7, command))
        pr8 = Process(target=match_road_busstop, args=(list_line_[63000:72000], 'road', 8, command))
        pr9 = Process(target=match_road_busstop, args=(list_line_[72000:81000], 'road', 9, command))
        pr10 = Process(target=match_road_busstop, args=(list_line_[81000:90000], 'road', 10, command))
        pr11 = Process(target=match_road_busstop, args=(list_line_[90000:], 'road', 11, command))

        pr1.start(), pr2.start(), pr3.start(), pr4.start(), pr5.start()
        pr6.start(), pr7.start(), pr8.start(), pr9.start(), pr10.start(), pr11.start()

        pr1.join(), pr2.join(), pr3.join(), pr4.join(), pr5.join()
        pr6.join(), pr7.join(), pr8.join(), pr9.join(), pr10.join(), pr11.join()


def running_bussstop(command):
    if command == 'twitter':
        pr1 = Process(target=match_road_busstop, args=(list_line_[0:21006], 'busstop', 1))
        pr2 = Process(target=match_road_busstop, args=(list_line_[21006:42003], 'busstop', 2))
        pr3 = Process(target=match_road_busstop, args=(list_line_[42003:63000], 'busstop', 3))
        pr4 = Process(target=match_road_busstop, args=(list_line_[63000:84006], 'busstop', 4))
        pr5 = Process(target=match_road_busstop, args=(list_line_[84006:105003], 'busstop', 5))
        pr6 = Process(target=match_road_busstop, args=(list_line_[105003:126000], 'busstop', 6))
        pr7 = Process(target=match_road_busstop, args=(list_line_[126000:147006], 'busstop', 7))
        pr8 = Process(target=match_road_busstop, args=(list_line_[147006:168003], 'busstop', 8))
        pr9 = Process(target=match_road_busstop, args=(list_line_[168003:189000], 'busstop', 9))
        pr10 = Process(target=match_road_busstop, args=(list_line_[189000:210006], 'busstop', 10))
        pr11 = Process(target=match_road_busstop, args=(list_line_[210006:], 'busstop', 11))

        pr1.start(), pr2.start(), pr3.start(), pr4.start(), pr5.start()
        pr6.start(), pr7.start(), pr8.start(), pr9.start(), pr10.start(), pr11.start()

        pr1.join(), pr2.join(), pr3.join(), pr4.join(), pr5.join()
        pr6.join(), pr7.join(), pr8.join(), pr9.join(), pr10.join(), pr11.join()

    elif command == 'sgforums':
        pr1 = Process(target=match_road_busstop, args=(list_line_[0:3000], 'busstop', 1))
        pr2 = Process(target=match_road_busstop, args=(list_line_[3000:6000], 'busstop', 2))
        pr3 = Process(target=match_road_busstop, args=(list_line_[6000:9000], 'busstop', 3))
        pr4 = Process(target=match_road_busstop, args=(list_line_[9000:12000], 'busstop', 4))
        pr5 = Process(target=match_road_busstop, args=(list_line_[12000:15000], 'busstop', 5))
        pr6 = Process(target=match_road_busstop, args=(list_line_[15000:18000], 'busstop', 6))
        pr7 = Process(target=match_road_busstop, args=(list_line_[18000:21000], 'busstop', 7))
        pr8 = Process(target=match_road_busstop, args=(list_line_[21000:24000], 'busstop', 8))
        pr9 = Process(target=match_road_busstop, args=(list_line_[24000:27000], 'busstop', 9))
        pr10 = Process(target=match_road_busstop, args=(list_line_[27000:30000], 'busstop', 10))
        pr11 = Process(target=match_road_busstop, args=(list_line_[30000:], 'busstop', 11))

        pr1.start(), pr2.start(), pr3.start(), pr4.start(), pr5.start()
        pr6.start(), pr7.start(), pr8.start(), pr9.start(), pr10.start(), pr11.start()

        pr1.join(), pr2.join(), pr3.join(), pr4.join(), pr5.join()
        pr6.join(), pr7.join(), pr8.join(), pr9.join(), pr10.join(), pr11.join()

    elif command == 'facebook':
        pr1 = Process(target=match_road_busstop, args=(list_line_[0:9000], 'busstop', 1, command))
        pr2 = Process(target=match_road_busstop, args=(list_line_[9000:18000], 'busstop', 2, command))
        pr3 = Process(target=match_road_busstop, args=(list_line_[18000:27000], 'busstop', 3, command))
        pr4 = Process(target=match_road_busstop, args=(list_line_[27000:36000], 'busstop', 4, command))
        pr5 = Process(target=match_road_busstop, args=(list_line_[36000:45000], 'busstop', 5, command))
        pr6 = Process(target=match_road_busstop, args=(list_line_[45000:54000], 'busstop', 6, command))
        pr7 = Process(target=match_road_busstop, args=(list_line_[54000:63000], 'busstop', 7, command))
        pr8 = Process(target=match_road_busstop, args=(list_line_[63000:72000], 'busstop', 8, command))
        pr9 = Process(target=match_road_busstop, args=(list_line_[72000:81000], 'busstop', 9, command))
        pr10 = Process(target=match_road_busstop, args=(list_line_[81000:90000], 'busstop', 10, command))
        pr11 = Process(target=match_road_busstop, args=(list_line_[90000:], 'busstop', 11, command))

        pr1.start(), pr2.start(), pr3.start(), pr4.start(), pr5.start()
        pr6.start(), pr7.start(), pr8.start(), pr9.start(), pr10.start(), pr11.start()

        pr1.join(), pr2.join(), pr3.join(), pr4.join(), pr5.join()
        pr6.join(), pr7.join(), pr8.join(), pr9.join(), pr10.join(), pr11.join()


if __name__ == '__main__':
    #######################################################################################
    #######################################################################################
    # TWITTER
    # sql = load_sql(command='twitter')
    # list_row = table_SQL(sql)
    # list_line = filtering_text_demo(list_row)
    # list_line_ = list_line
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter/crf_features'
    #
    # print len(list_line_)
    # running_road(command='twitter')
    # running_bussstop(command='twitter')

    #######################################################################################
    #######################################################################################
    # SGFORUMS
    # sql = load_sql(command='sgforums')
    # list_row = table_SQL(sql)
    # list_line = filtering_text_demo(list_row, 'sgforums')
    # list_line_ = list_line
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums/crf_features'
    #
    # print len(list_line_)
    # running_road(command='sgforums')
    # running_bussstop(command='sgforums')

    #######################################################################################
    #######################################################################################
    # FACEBOOK
    sql = load_sql(command='facebook')
    list_row = table_SQL(sql)
    list_line = filtering_text_demo(list_row, 'facebook')
    list_line_ = list_line
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook/crf_features'

    print len(list_line_)
    # running_road(command='facebook')
    running_bussstop(command='facebook')
