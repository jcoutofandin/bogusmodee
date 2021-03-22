##########################################################################
#
# Python 3 script   : BogusModee.py - Games
#
##########################################################################
# Description
#
# This script will display scores of games played.
##########################################################################
import pymysql
import os
import time
import getpass
import datetime

class JobDb:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = None
        self.login_id = 0
        self.login_name = ''
        self.login_type = ''

    def open_db(self):
        # Open database connection
        self.db = pymysql.connect(host = self.host, user = self.user, password = self.password , database=self.database)

    def close_db(self):
        # disconnect from server
        self.db.close()

    def SQL_fetch_one(self, sql):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.db.cursor()

            # execute SQL query using execute() method.
            cursor.execute(sql)

            # Fetch a single row using fetchone() method.
            data = cursor.fetchone()
            return data
        except:
            print("Error: unable to fetch data")

    def SQL_fetch_all(self, sql):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.db.cursor()
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")

    def SQL_execute(self, sql):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.db.cursor()
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            return True
        except:
            # Rollback in case there is any error
            self.db.rollback()
            print("Error: DB rollback")
            return False

    def display_version(self):
        sql = "SELECT VERSION()"
        data = self.SQL_fetch_one(sql)

        print("Database version : %s " % data)

    def display_gamer(self):
        sql = "SELECT * FROM gamer"
        results = self.SQL_fetch_all(sql)
        for row in results:
            gamer_id = row[0]
            login_id = row[1]
            first_name = row[2]
            last_name = row[3]
            email = row[4]
            birthdate = row[5]
            country = row[6]
            town = row[7]
            gender = row[8]
            created_at = row[9]
            # Now print fetched resul
            print("gamer_id = %d,login_id = %d,first_name = %s,last_name = %s,email = %s,birthdate = %s,country = %s,town = %s,gender = %s,created_at = %s" % \
            (gamer_id, login_id, first_name, last_name, email, birthdate, country, town, gender, created_at ))

################################################################################
# functions
################################################################################

def validate(date_text, date_format='%Y-%m-%d', date_display='YYYY-MM-DD'):
    try:
        datetime.datetime.strptime(date_text, date_format)
    except ValueError:
        raise ValueError("Incorrect data format, should be " + date_display)

def test_field(t_field, t_label, t_type, t_len_min=0, t_len_max=0, t_pass='N'):
    ret = True
    t_ret=()

    try:
        if t_pass == 'Y':
            t_field = getpass.getpass(prompt='      ' + t_label + ' : ')
        else:
            t_field = input(' ' * 6 + t_label + ' : ')

        #print(' ' * 6 + 't_field ->', t_field)

        if t_type == 'alpha':
            if not t_field.isalpha():
                print(' ' * 6 + t_label + ' invalid! You must enter an alphabetical value')
                ret = False

        if t_type == 'alnum':
            if not t_field.isalnum():
                print(' ' * 6 + t_label + ' invalid! You must enter an alphanumeric value')
                ret = False

        if t_type == 'digit':
            if not t_field.isdigit():
                print(' ' * 6 + t_label + ' invalid! You must enter a numeric value')
                ret = False
            else:
                t_field = int(t_field)

        if t_len_max > 0 and t_type != 'digit':
            if len(t_field) < t_len_min or len(t_field) > t_len_max:
                print(' ' * 6 + t_label + ' invalid! The number of characters must be between ' + str(t_len_min) + ' and ' + str(t_len_max))
                ret = False

    except ValueError:
        print(' ' * 6 + t_label + ' invalid! Value error.')
        time.sleep(1)
        ret = False
    except Exception as error:
        print(' ' * 6 + t_label + ' invalid! Exception error.')
        print('ERROR', error)
        ret = False

    if ret == False:
        t_field=''
        t_ret=(ret, t_field)
    else:
        t_ret=(ret, t_field)

    return t_ret

def cal_shift_list(len_list=0, offset=0, i_beg=0, i_end=0, direction=''):
    if len_list != 0 and offset != 0:
        if direction == 'B':
            i_beg -=offset
            if i_beg < 0:
                i_beg = 0
            i_end = i_beg + offset
            if i_end > len_list:
                i_end = len_list
        elif direction == 'F':
            i_beg = i_end
            i_end = i_beg + offset
            if i_end > len_list:
                i_beg = len_list - offset
                i_end = len_list

    return i_beg, i_end

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def menu_header(job):

    # now, to clear the screen
    cls()
    #print('      ==========     '.center(65), ' ' * 20, 'login :', job.login_name)
    #print('----- BogusModee ----'.center(65))
    #print('      ==========     '.center(65))
    print('    ____                         __  ___          _          '.center(80), ' ' * 5, 'login :', job.login_name)
    print('   / __ )____  ____ ___  _______/  |/  /___  ____/ /__  ___  '.center(80))
    print('  / __  / __ \/ __ `/ / / / ___/ /|_/ / __ \/ __  / _ \/ _ \ '.center(80))
    print(' / /_/ / /_/ / /_/ / /_/ (__  ) /  / / /_/ / /_/ /  __/  __/ '.center(80))
    print('/_____/\____/\__, /\__,_/____/_/  /_/\____/\__,_/\___/\___/  '.center(80))
    print('            /____/                                           '.center(80))
    print('\n\n\n')

def display_my_ranking_for_a_game(job):
    flag_redisplay = True
    cpt = 0
    game_id = ''
    title  = ''
    rank = 0

    #sql = "SELECT game_id, title FROM game order by game_id"
    #sql = "SELECT g.game_id, g.title FROM game g, score s WHERE g.game_id = s.game_id AND s.login_id = '%s' ORDER BY g.game_id" % (job.login_id)
    sql = "SELECT g.game_id, g.title, s.score FROM game g, score s WHERE g.game_id = s.game_id AND s.login_id = '%s' ORDER BY g.game_id" % (job.login_id)
    results = job.SQL_fetch_all(sql)

    len_results = len(results)
    offset = 8
    i_beg = 0

    if offset > len_results:
        offset = len_results

    i_end = i_beg + offset

    '''
    print('results ->', results)
    print('results [0][0] ->', results[0][0])
    print('results [0][1] ->', results[0][1])
    print('results [0][2] ->', results[0][2])
    '''

    while flag_redisplay and cpt < 3:
        menu_header(job)

        #print(' ' * 5 + '          My ranking for a game')
        #print(' ' * 5 + '          -- ------- --- - ----\n\n')
        #print(' ' * 5 + '| Game_id |            Title             |')
        #print(' ' * 5 + ' --------- ------------------------------')

        print(' ' * 5 + '                My ranking for a game')
        print(' ' * 5 + '                -- ------- --- - ----\n\n')
        print(' ' * 5 + '| Game_id |            Title             |     Score     |')
        print(' ' * 5 + ' --------- ------------------------------ --------------- ')

        if results == ():
            print(' ' * 5 + ' No game')
        else:
            for i in range (i_beg, i_end):
                r_game_id = results[i][0]
                r_title = results[i][1]
                r_score = results[i][2]
                # Now print fetched resul
                #print(' ' * 5 + '|' + str(r_game_id).center(9) + '|' + r_title.center(30) + '|')
                print(' ' * 5 + '|' + str(r_game_id).center(9) + '|' + r_title.center(30) + '|' + str(int(r_score)).center(15) + '|')

            print('\n')
            print(' ' * 5 + '(B)ackward <<< List >>> (F)orward'+ ' ' * 12 + '(' + str(i_end) + '/' + str(len_results) + ') Row(s)')
            print('\n\n')

            if game_id == '':
                try:
                    #game_id = int(input(' ' * 5 + ' Game_id : '))
                    game_id = input(' ' * 5 + ' Game_id : ')
                    if not game_id.isdigit():
                        if game_id.capitalize().find('B') != -1:
                            i_beg, i_end = cal_shift_list(len_list=len_results, offset=offset, i_beg=i_beg, i_end=i_end, direction='B')
                            game_id = ''
                            continue
                        elif game_id.capitalize().find('F') != -1:
                            i_beg, i_end = cal_shift_list(len_list=len_results, offset=offset, i_beg=i_beg, i_end=i_end, direction='F')
                            game_id = ''
                            continue
                        else:
                            print(' ' * 6 + 'Game_id invalid! You must enter an integer value.')
                            time.sleep(1)
                            game_id = ''
                            cpt += 1
                            continue
                    else:
                        game_id = int(game_id)
                except ValueError:
                    print(' ' * 6 + 'Game_id invalid! You must enter an integer value.')
                    time.sleep(1)
                    game_id = ''
                    cpt += 1
                    continue
                except Exception as error:
                    print(' ' * 6 + 'Game_id invalid!')
                    print('ERROR', error)
                    time.sleep(1)
                    game_id = ''
                    cpt += 1
                    continue

                #sql = "SELECT game_id, title FROM game WHERE game_id = '%d'" % (game_id)
                sql = "SELECT g.game_id, g.title FROM game g, score s WHERE g.game_id = s.game_id AND s.game_id = '%d' AND s.login_id = '%s'" % (game_id, job.login_id)
                data = job.SQL_fetch_one(sql)
                if data == None:
                    print(' ' * 6 + 'Game_id invalid!')
                    time.sleep(1)
                    game_id = ''
                    cpt += 1
                    continue
                
                cpt = 0
                game_id = data[0]
                title  = data[1]
            else:
                print(' ' * 5 + ' Game_id : %s' % (game_id))


            sql = "SELECT COUNT(*) FROM score WHERE game_id = '%d' AND login_id = '%s'"  % (game_id, job.login_id)
            data = job.SQL_fetch_one(sql)
            if data[0] == 0:
                print('\n')
                print(' ' * 6 + 'Unranked for game "' + title+ '"')
            else:
                sql = "SELECT COUNT(*) FROM score WHERE game_id = '%d' AND score > (SELECT score FROM score WHERE game_id = '%d' AND login_id = '%s')" % (game_id, game_id, job.login_id)

                data = job.SQL_fetch_one(sql)
                rank = data[0]
                rank += 1
                print('\n')
                print(' ' * 6 + 'My ranking for game "' + title + '" is :', rank)

        print('\n\n')

        print(' ' * 5 + 'ENTER ==> New search')
        print(' ' * 5 + 'R     ==> RETURN')
        print('\n')

        rep = input(' ' * 5 + 'Choice ==> ').capitalize()
        if rep == '':
            game_id = ''
        elif rep == 'B':
            i_beg, i_end = cal_shift_list(len_list=len_results, offset=offset, i_beg=i_beg, i_end=i_end, direction='B')
        elif rep == 'F':
            i_beg, i_end = cal_shift_list(len_list=len_results, offset=offset, i_beg=i_beg, i_end=i_end, direction='F')
        elif rep == 'R':
            flag_redisplay = False

    return ''

def display_top_5_ranking_of_all_games(job):
    flag_redisplay = True

    while flag_redisplay:
        menu_header(job)

        print(' ' * 5 + '                      Top 5 ranking of all games')
        print(' ' * 5 + '                      --- - ------- -- --- -----\n\n')
        print(' ' * 5 + '| Game_id |            Title             | Maximum score |         Gamer      |')
        print(' ' * 5 + ' --------- ------------------------------ --------------   ------------------')

        #sql = "SELECT g.game_id, g.title FROM game g, score s WHERE g.game_id = s.game_id AND s.login_id = '%s' ORDER BY g.game_id" % (job.login_id)
        #sql = "SELECT g.game_id, g.title, MAX(s.score) FROM game g, score s WHERE g.game_id = s.game_id GROUP BY g.game_id, g.title ORDER BY g.game_id"
        #sql = "SELECT g.game_id, g.title, MAX(s.score) FROM game g, score s WHERE g.game_id = s.game_id GROUP BY g.game_id, g.title ORDER BY MAX(s.score) DESC, g.game_id"
        #sql = "SELECT g.game_id, g.title, s.score, s.nickname FROM game g, score s WHERE g.game_id = s.game_id ORDER BY s.score DESC, g.game_id, s.nickname"
        sql = "SELECT g.game_id, g.title, s.score, l.login_name FROM game g, score s, login l WHERE l.login_id = s.login_id AND g.game_id = s.game_id ORDER BY s.score DESC, g.game_id, l.login_name"
        results = job.SQL_fetch_all(sql)

        cpt = 0
        for row in results:
            cpt += 1
            game_id = row[0]
            title = row[1]
            score_max = row[2]
            login_name = row[3]

            '''
            login_name = ''

            sql = "SELECT l.login_name FROM login l, score s WHERE l.login_id = s.login_id AND s.game_id = '%d' AND s.score = '%d'" % (game_id, score_max)
            data = job.SQL_fetch_one(sql)
            if data == None:
                login_name = 'Unknow'
            else:
                login_name = data[0]
            '''

            # Now print fetched resul
            print(' ' * 5 + '|' + str(game_id).center(9) + '|' + title.center(30) + '|' + str(int(score_max)).center(15) + '|' + login_name.center(20) + '|')

            if cpt == 5:
                break

        print('\n\n\n')

        print(' ' * 5 + 'R     ==> RETURN')
        print('\n')

        rep = input(' ' * 5 + 'Choice ==> ').capitalize()
        if rep == 'R':
            flag_redisplay = False

    return ''

def display_Provide_my_score_of_my_game(job):
    flag_redisplay = True
    flag_upd = False
    message_maj = ''
    cpt = 0
    game_id = ''
    title  = ''
    score = 0
    results_list = []
    offset = 8
    i_beg = 0

    while flag_redisplay and cpt < 3:
        menu_header(job)

        print(' ' * 5 + '            Provide the score of my game')
        print(' ' * 5 + '            ------- --- ----- -- -- ----\n\n')
        print(' ' * 5 + '| Game_id |            Title             |     Score     |')
        print(' ' * 5 + ' --------- ------------------------------ --------------- ')

        #sql = "SELECT g.game_id, g.title FROM game g, score s WHERE g.game_id = s.game_id AND s.login_id = '%s' ORDER BY g.game_id" % (job.login_id)
        sql = "SELECT game_id, title FROM game ORDER BY game_id"
        results = job.SQL_fetch_all(sql)

        results_list = []
        for row in results:
            results_list.append(list(row))

        len_results_list = len(results_list)

        if offset > len_results_list:
            offset = len_results_list

        for row in results_list:
            r_game_id = row[0]
            r_title = row[1]

            # Find score
            r_score = ''

            sql = "SELECT s.score FROM score s, game g WHERE s.game_id = g.game_id AND s.login_id = '%d' AND s.game_id = '%d'" % (job.login_id, r_game_id)
            data = job.SQL_fetch_one(sql)
            if data == None:
                r_score = 'Unknow'
            else:
                r_score = data[0]

            # add r_score to row of results_list
            row.append(r_score)

        if results == ():
            print(' ' * 5 + ' No game')
        else:
            i_end = i_beg + offset

            for i in range (i_beg, i_end):
                r_game_id = results_list[i][0]
                r_title = results_list[i][1]
                r_score = results_list[i][2]
                # Now print fetched resul
                #print(' ' * 5 + '|' + str(r_game_id).center(9) + '|' + r_title.center(30) + '|')
                #print(' ' * 5 + '|' + str(r_game_id).center(9) + '|' + r_title.center(30) + '|' + str(int(r_score)).center(15) + '|')
                # Now print fetched resul
                if r_score == 'Unknow':
                    print(' ' * 5 + '|' + str(r_game_id).center(9) + '|' + r_title.center(30) + '|' + ' '.center(15) + '|')
                else:
                    print(' ' * 5 + '|' + str(r_game_id).center(9) + '|' + r_title.center(30) + '|' + str(int(r_score)).center(15) + '|')

            print('\n')
            print(' ' * 5 + '(B)ackward <<< List >>> (F)orward'+ ' ' * 12 + '(' + str(i_end) + '/' + str(len_results_list) + ') Row(s)')
            print('\n\n')

            if game_id == '':
                try:
                    #game_id = int(input(' ' * 5 + ' Game_id : '))
                    game_id = input(' ' * 5 + ' Game_id : ')
                    if not game_id.isdigit():
                        if game_id.capitalize().find('B') != -1:
                            i_beg, i_end = cal_shift_list(len_list=len_results_list, offset=offset, i_beg=i_beg, i_end=i_end, direction='B')
                            game_id = ''
                            continue
                        elif game_id.capitalize().find('F') != -1:
                            i_beg, i_end = cal_shift_list(len_list=len_results_list, offset=offset, i_beg=i_beg, i_end=i_end, direction='F')
                            game_id = ''
                            continue
                        else:
                            print(' ' * 6 + 'Game_id invalid! You must enter an integer value.')
                            time.sleep(1)
                            game_id = ''
                            cpt += 1
                            continue
                    else:
                        game_id = int(game_id)
                except ValueError:
                    print(' ' * 6 + 'Game_id invalid! You must enter an integer value.')
                    time.sleep(1)
                    game_id = ''
                    cpt += 1
                    continue
                except Exception as error:
                    print(' ' * 6 + 'Game_id invalid!')
                    print('ERROR', error)
                    time.sleep(1)
                    game_id = ''
                    cpt += 1
                    continue

                sql = "SELECT game_id, title FROM game WHERE game_id = '%d'" % (game_id)
                data = job.SQL_fetch_one(sql)
                if data == None:
                    print(' ' * 6 + 'Game_id invalid!')
                    time.sleep(1)
                    game_id = ''
                    cpt += 1
                    continue
                
                cpt = 0
                game_id = data[0]
            else:
                print(' ' * 5 + ' Game_id : %s' % (game_id))

            if score == 0:
                ret, score = test_field(t_field=score, \
                        t_label='  Score', t_type='digit', t_len_min=0, t_len_max=0, t_pass='N')  

                if ret == False:
                    time.sleep(1)
                    score = 0
                    cpt += 1
                    continue

                if score <= 0:
                    print(' ' * 6 + '  Score invalid! It must be superior to 0.')
                    time.sleep(1)
                    score = 0
                    cpt += 1
                    continue
                elif score > 1000000:
                    print(' ' * 6 + '  Score invalid! It must be inferior to 1000000.')
                    time.sleep(1)
                    score = 0
                    cpt += 1
                    continue
                '''
                try:
                    score = int(input(' ' * 5 + ' Score   : '))
                    if score <= 0:
                        print(' ' * 6 + 'Score invalid! It must be superior to 0.')
                        time.sleep(1)
                        score = 0
                        cpt += 1
                        continue
                    elif score > 1000000:
                        print(' ' * 6 + 'Score invalid! It must be inferior to 1000000.')
                        time.sleep(1)
                        score = 0
                        cpt += 1
                        continue
                except ValueError:
                    print(' ' * 6 + 'score invalid! You must enter an integer value.')
                    time.sleep(1)
                    score = 0
                    cpt += 1
                    continue
                except Exception as error:
                    print(' ' * 6 + 'Score invalid!')
                    print('ERROR', error)
                    time.sleep(1)
                    score = 0
                    cpt += 1
                    continue
                '''

                cpt = 0
            else:
                print(' ' * 5 + ' Score   : %d' % (score))

            if flag_upd == False:
                flag_upd = True
                #print(' ' * 5 + '|' + str(game_id).center(9) + '|' + job.login_name.center(30) + '|')
                sql = "SELECT score FROM score WHERE login_id = '%d' AND game_id = '%d'" % (job.login_id, game_id)
                data = job.SQL_fetch_one(sql)
                if data == None:
                    sql = "INSERT INTO score (login_id, game_id, score, created_at) \
                            VALUES ('%d', '%d', '%d', NOW())" % \
                            (job.login_id, game_id, score)
                    ret = job.SQL_execute(sql)
                    if ret == False:
                        #print(' ' * 6 + 'Error Insertion !')
                        message_maj = 'Error Insertion !'
                    else:
                        #print(' ' * 6 + 'Successful Insertion !')
                        message_maj = 'Successful Insertion !'
                else:
                    sql = "UPDATE score SET score = '%d', created_at = NOW() \
                            WHERE login_id = '%d' AND game_id = '%d'" % \
                            (score, job.login_id, game_id)
                    ret = job.SQL_execute(sql)
                    if ret == False:
                        #print(' ' * 6 + 'Error Update !')
                        message_maj = 'Error Update !'
                    else:
                        #print(' ' * 6 + 'Successful Update !')
                        message_maj = 'Successful Update !'

                print(' ' * 6 + '%s' % (message_maj))
                #time.sleep(1)
                continue
            else:
                print(' ' * 6 + '%s' % (message_maj))

        print('\n\n')

        print(' ' * 5 + 'ENTER ==> New Update')
        print(' ' * 5 + 'R     ==> RETURN')
        print('\n')

        rep = input(' ' * 5 + 'Choice ==> ').capitalize()
        if rep == '':
            game_id = ''
            score = 0
            flag_upd = False
            message_maj = ''
        elif rep == 'B':
            i_beg, i_end = cal_shift_list(len_list=len_results_list, offset=offset, i_beg=i_beg, i_end=i_end, direction='B')
        elif rep == 'F':
            i_beg, i_end = cal_shift_list(len_list=len_results_list, offset=offset, i_beg=i_beg, i_end=i_end, direction='F')
        elif rep == 'R':
            flag_redisplay = False

    return ''

def menu_main(job):

    rep = ''

    while rep not in ['Q', 'R', '1', '2', '3']:
        menu_header(job)
        print(' ' * 5 + '1 ==> My ranking for a game')
        print(' ' * 5 + '2 ==> Top 5 rankings of all games')
        print(' ' * 5 + '3 ==> Provide the score of my game')
        print(' ' * 5 + 'R ==> RETURN')
        print(' ' * 5 + 'Q ==> QUIT')
        print('\n')

        rep = input(' ' * 5 + 'Choice ==> ').capitalize()

        if rep == '1':
            rep = display_my_ranking_for_a_game(job)
        elif rep == '2':
            rep = display_top_5_ranking_of_all_games(job)
        elif rep == '3':
            rep = display_Provide_my_score_of_my_game(job)

    return rep

def menu_login(job):

    flag_redisplay = True
    cpt = 0
    ret = False
    job.login_name = ''
    login_pwd  = ''
    job.login_type = ''

    while flag_redisplay and cpt < 3:
        menu_header(job)

        if job.login_name == '':
            name = input(' ' * 5 + ' Login Name : ')

            sql = "SELECT login_id, login_name, login_pwd, login_type FROM login WHERE login_name = '%s'" % (name)
            data = job.SQL_fetch_one(sql)
            if data == None:
                print(' ' * 6 + 'Login Name invalid!')
                time.sleep(1)
                cpt += 1
                continue
            
            cpt = 0
            job.login_id = data[0]
            job.login_name = data[1]
            login_pwd  = data[2]
            job.login_type = data[3]

            '''
            print("login_id : %d " % job.login_id)
            print("login_name : %s " % job.login_name)
            print("login_pwd : %s " % login_pwd)
            print("login_type : %s " % job.login_type)
            '''
        else:
            print(' ' * 5 + ' login Name : %s' % (job.login_name))

        #pwd = input(' ' * 5 + ' password : ')
        pwd = getpass.getpass(prompt='      Password   : ')

        if pwd != login_pwd:
            print(' ' * 6 + 'Password invalid!')
            time.sleep(1)
            cpt += 1
            continue
        else:
            flag_redisplay = False
            ret = True

    return ret

def cancel_entry():
    c_rep = ''
    c_ret = ''
    c_cpt = 0
    c_flag_redisplay = True
    c_return=()

    print('\n')
    print(' ' * 5 + 'Y/N ==> Cancel entries and return to the previous screen?') 
    print('\n')

    c_rep = input(' ' * 5 + 'Choice ==> ').capitalize()
    if c_rep == 'Y':
        c_flag_redisplay = False

    c_return=(c_ret, c_cpt, c_flag_redisplay)

    return c_return

def i_want_to_register_to_the_application(job):

    flag_redisplay = True
    flag_upd_login = True
    flag_read_login = True
    flag_upd_gamer = True
    flag_validation = True
    cpt = 0
    #cpt_pwd_verif = 0
    ret = False
    rep = ''
    job.login_id = 0
    job.login_name = ''
    login_pwd  = ''
    login_pwd_verif = ''
    job.login_type = 'gamer'
    first_name = ''
    last_name = ''
    email = ''
    birthdate = ''
    country = ''
    town = ''
    gender = ''

    while flag_redisplay:
        menu_header(job)
        '''
        if cpt < 3:
            menu_header(job)
        else:
            rep = ''
            while rep not in ['Y', 'N']:
                print('\n')
                print(' ' * 5 + 'Y/N ==> Cancel entries and return to the previous screen?') 
                print('\n')

                rep = input(' ' * 5 + 'Choice ==> ').capitalize()
                #print('rep ->', rep)
                if rep == 'Y':
                    #print('2rep ->', rep)
                    flag_redisplay = False
                    cpt = 0
                    ret = ''
                    continue
                elif rep == 'N':
                    cpt = 0
                    continue
            continue
        '''

        if flag_validation == False:
            if job.login_name == '' and login_pwd  == '' and login_pwd_verif == '' and first_name == '' and \
                    last_name == '' and email == '' and birthdate == '' and country == '' and town == '' and gender == '':
                flag_validation == True

        if flag_validation == False:
            '''
            print(' ' * 6 + '    Login Name : %s' % (job.login_name))
            print()
            print(' ' * 6 + '    Password   : *****')
            print()
            print(' ' * 6 + '    First Name : %s' % (first_name))
            print()
            print(' ' * 6 + '    Last Name  : %s' % (last_name))
            print()
            print(' ' * 6 + '    Email      : %s' % (email))
            print()
            print(' ' * 6 + '    Birthdate  : %s' % (birthdate))
            print()
            print(' ' * 6 + '    Country    : %s' % (country))
            print()
            print(' ' * 6 + '    Town       : %s' % (town))
            print()
            print(' ' * 6 + '    Gender     : %s' % (gender))
            #
            '''
            if job.login_name != '':
                print(' ' * 6 + '    Login Name : %s' % (job.login_name))
            else:
                print(' ' * 6 + '    Login Name : %s' % (old_login_name))
            if login_pwd  != '':
                print()
                print(' ' * 6 + '    Password   : *****')
            else:
                print()
                print(' ' * 6 + '    Password   :') 
            if login_pwd_verif != '':
                pass
            if first_name != '':
                print()
                print(' ' * 6 + '    First Name : %s' % (first_name))
            else:
                print()
                print(' ' * 6 + '    First Name : %s' % (old_first_name))
            if last_name != '':
                print()
                print(' ' * 6 + '    Last Name  : %s' % (last_name))
            else:
                print()
                print(' ' * 6 + '    Last Name  : %s' % (old_last_name))
            if email != '':
                print()
                print(' ' * 6 + '    Email      : %s' % (email))
            else:
                print()
                print(' ' * 6 + '    Email      : %s' % (old_email))
            if birthdate != '':
                print()
                print(' ' * 6 + '    Birthdate  : %s' % (birthdate))
            else:
                print()
                print(' ' * 6 + '    Birthdate  : %s' % (old_birthdate))
            if country != '':
                print()
                print(' ' * 6 + '    Country    : %s' % (country))
            else:
                print()
                print(' ' * 6 + '    Country    : %s' % (old_country))
            if town != '':
                print()
                print(' ' * 6 + '    Town       : %s' % (town))
            else:
                print()
                print(' ' * 6 + '    Town       : %s' % (old_town))
            if gender != '':
                print()
                print(' ' * 6 + '    Gender     : %s' % (gender))
            else:
                print()
                print(' ' * 6 + '    Gender     : %s' % (old_gender))
            print('\n' + ' ' * 6 + '    *********** Field update ***********')

        if job.login_name == '':
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, job.login_name = test_field(t_field=job.login_name, \
                    t_label='    Login Name', t_type='alnum', t_len_min=3, t_len_max=20, t_pass='N')  

            if ret == False:
                time.sleep(2)
                job.login_name = ''
                cpt += 1
                continue

            sql = "SELECT login_id, login_name, login_pwd, login_type FROM login WHERE login_name = '%s'" % (job.login_name)
            data = job.SQL_fetch_one(sql)
            if data != None:
                print(' ' * 10 + 'Login Name already existing!')
                time.sleep(2)
                job.login_name = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print(' ' * 6 + '    Login Name : %s' % (job.login_name))

        if login_pwd  == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, login_pwd = test_field(t_field=login_pwd, \
                    t_label='    Password  ', t_type=None, t_len_min=3, t_len_max=50, t_pass='Y')  

            if ret == False:
                time.sleep(2)
                login_pwd = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Password   : *****')

        if login_pwd_verif == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                login_pwd = ''
                continue

            ret, login_pwd_verif = test_field(t_field=login_pwd_verif, \
                    t_label='    Password verification  ', t_type=None, t_len_min=3, t_len_max=50, t_pass='Y')  

            if ret == False:
                time.sleep(2)
                login_pwd_verif = ''
                cpt += 1
                continue

            if login_pwd_verif != login_pwd:
                print(' ' * 10 + 'Password not identical')
                time.sleep(2)
                login_pwd_verif = ''
                cpt += 1
                continue
                '''
                cpt_pwd_verif += 1
                if cpt_pwd_verif == 3:
                    login_pwd = ''
                    login_pwd_verif = ''
                    cpt_pwd_verif = 0
                    cpt = 0
                continue
                '''

            #cpt_pwd_verif = 0
            cpt = 0
            continue

        if first_name == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, first_name = test_field(t_field=first_name, \
                    t_label='    First Name', t_type=None, t_len_min=3, t_len_max=30, t_pass='N')  

            if ret == False:
                time.sleep(2)
                first_name = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    First Name : %s' % (first_name))

        if last_name == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, last_name = test_field(t_field=last_name, \
                    t_label='    Last Name ', t_type=None, t_len_min=3, t_len_max=30, t_pass='N')  

            if ret == False:
                time.sleep(2)
                last_name = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Last Name  : %s' % (last_name))

        if email == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, email = test_field(t_field=email, \
                    t_label='    E-mail    ', t_type=None, t_len_min=3, t_len_max=30, t_pass='N')  

            if ret == False:
                time.sleep(2)
                email = ''
                cpt += 1
                continue

            cpt = 0

            pos = email.find('@')
            if pos == -1:
                print(' ' * 10 + 'Email invalid! Must have the "@" character')
                time.sleep(2)
                email = ''
                cpt += 1
                continue

            cpt = 0

            if email[pos:].find('.') == -1:
                print(' ' * 10 + 'Email invalid! Must have the "." character after the character "@"')
                time.sleep(2)
                email = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Email      : %s' % (email))

        if birthdate == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, birthdate = test_field(t_field=birthdate, \
                    t_label='    Birthdate (format YYYY-MM-DD)', t_type=None, t_len_min=10, t_len_max=10, t_pass='N')  

            if ret == False:
                time.sleep(2)
                birthdate = ''
                cpt += 1
                continue

            cpt = 0

            try:
                validate(birthdate, date_format='%Y-%m-%d', date_display='YYYY-MM-DD')
            except ValueError as error:
                print(' ' * 10 + 'Birthdate invalid!', error)
                time.sleep(2)
                birthdate = ''
                cpt += 1
                continue

            cpt = 0

            year, month, day = birthdate.split('-')

            if int(year) < 1910 or int(year) > 2010:
                print(' ' * 10 + 'Birthdate invalid! The year must be between 1910 and 2010')
                time.sleep(2)
                birthdate = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Birthdate  : %s' % (birthdate))

        if country == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, country = test_field(t_field=country, \
                    t_label='    Country   ', t_type=None, t_len_min=3, t_len_max=30, t_pass='N')  

            if ret == False:
                time.sleep(2)
                country = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Country    : %s' % (country))

        if town == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, town = test_field(t_field=town, \
                    t_label='    Town      ', t_type=None, t_len_min=3, t_len_max=30, t_pass='N')  

            if ret == False:
                time.sleep(2)
                town = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Town       : %s' % (town))

        if gender == '':
            print()
            if cpt == 3:
                ret, cpt, flag_redisplay = cancel_entry()
                continue

            ret, gender = test_field(t_field=gender, \
                    t_label='    Gender    ', t_type='alpha', t_len_min=1, t_len_max=1, t_pass='N')  

            if ret == False:
                time.sleep(2)
                gender = ''
                cpt += 1
                continue

            gender = gender.upper()
            if gender not in ('MF'):
                print(' ' * 10 + 'Gender invalid! Must be "F" or "M" character')
                time.sleep(2)
                gender = ''
                cpt += 1
                continue

            cpt = 0
        else:
            if flag_validation == True:
                print()
                print(' ' * 6 + '    Gender     : %s' % (gender))

        if flag_validation == False:
            flag_validation = True
            continue

        if flag_validation == True:
            flag_validation = False
            rep = ''
            print('\n')
            print(' ' * 5 + 'Y      ==> Validation of entered data')
            print(' ' * 5 + 'N      ==> Cancel entries and return to the previous screen!')
            print(' ' * 5 + '1 .. 9 ==> Field update')
            print(' ' * 5 + '1) Login Name')
            print(' ' * 5 + '2) Password  ')
            print(' ' * 5 + '3) First Name')
            print(' ' * 5 + '4) Last Name ')
            print(' ' * 5 + '5) E-mail    ')
            print(' ' * 5 + '6) Birthdate ')
            print(' ' * 5 + '7) Country   ')
            print(' ' * 5 + '8) Town      ')
            print(' ' * 5 + '9) Gender    ')
            print('\n')

            rep = input(' ' * 5 + 'Choice ==> ').capitalize()
            if rep not in ['Y', 'N', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                rep = ''
                continue
            elif rep == 'Y':
                ret = ''
            elif rep == 'N':
                flag_redisplay = False
                ret = ''
                cpt = 0
                continue
            elif rep == '1':
                old_login_name = job.login_name
                job.login_name = ''
                cpt = 0
                continue
            elif rep == '2':
                old_login_pwd = login_pwd
                login_pwd = ''
                cpt = 0
                continue
            elif rep == '3':
                old_first_name = first_name
                first_name = ''
                cpt = 0
                continue
            elif rep == '4':
                old_last_name = last_name
                last_name = ''
                cpt = 0
                continue
            elif rep == '5':
                old_email = email
                email = ''
                cpt = 0
                continue
            elif rep == '6':
                old_birthdate = birthdate
                birthdate = ''
                cpt = 0
                continue
            elif rep == '7':
                old_country = country
                country = ''
                cpt = 0
                continue
            elif rep == '8':
                old_town = town
                town = ''
                cpt = 0
                continue
            elif rep == '9':
                old_gender = gender
                gender = ''
                cpt = 0
                continue
            else:
                flag_validation = True
                cpt = 0
                continue

        if flag_upd_login == True:
            sql = "INSERT INTO login (login_name, login_pwd, login_type, created_at) \
                    VALUES ('%s', '%s', '%s', NOW())" % \
                    (job.login_name, login_pwd, job.login_type)
            ret = job.SQL_execute(sql)
            if ret == False:
                print('\n' + ' ' * 6 + 'Insertion error in the login table!')
                flag_redisplay = False
                flag_upd_login = False
                ret = False
                input('\n\n' + ' ' * 5 + 'Enter  ==> Return')
                continue
            else:
                print('\n' + ' ' * 6 + 'Successful insertion in the login table!')
                flag_upd_login = False

        if flag_read_login == True:
            sql = "SELECT login_id FROM login WHERE login_name = '%s'" % (job.login_name)
            data = job.SQL_fetch_one(sql)
            if data == None:
                print('\n' + ' ' * 6 + "Error reading login table: login_id not found for login_name: '%s'!" % (job.login_name))
                flag_redisplay = False
                flag_read_login = False
                ret = False
                input('\n\n' + ' ' * 5 + 'Enter  ==> Return')
                continue
            else:
                job.login_id = data[0]
                flag_read_login = False

        if flag_upd_gamer == True:
            sql = "INSERT INTO gamer (login_id, first_name, last_name, email, birthdate, country, town, gender, created_at) \
                    VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW())" % \
                    (job.login_id, first_name, last_name, email, birthdate, country, town, gender)
            ret = job.SQL_execute(sql)
            if ret == False:
                print('\n' + ' ' * 6 + 'Insertion error in the gamer table!')
                # Begin -- Delete login table
                sql = "DELETE FROM login WHERE login_name = '%s'" % (job.login_name)
                ret = job.SQL_execute(sql)
                if ret == False:
                    print('\n' + ' ' * 6 + 'Delete error in the login table!')
                    flag_redisplay = False
                    flag_upd_gamer = False
                    ret = False
                    input('\n\n' + ' ' * 5 + 'Enter  ==> Return')
                    continue
                else:
                    print('\n' + ' ' * 6 + 'Successful delete in the login table!')
                # end -- Delete login table
                flag_redisplay = False
                flag_upd_gamer = False
                ret = False
                input('\n\n' + ' ' * 5 + 'Enter  ==> Return')
                continue
            else:
                print('\n' + ' ' * 6 + 'Successful Insertion in the gamer table!')
                flag_upd_gamer = False
                input('\n\n' + ' ' * 5 + 'Enter  ==> Return')

        flag_redisplay = False
        ret = True

    # end while

    return ret

def menu_init(job):

    rep = ''
    ret = False

    while rep not in ['Q', '1', '2']:
        menu_header(job)
        print(' ' * 5 + '1 ==> Login')
        print(' ' * 5 + '2 ==> Register')
        print(' ' * 5 + 'Q ==> QUIT')
        print('\n')

        rep = input(' ' * 5 + 'Choice ==> ').capitalize()
        if rep == '1':
            ret = menu_login(job)
            if ret == True:
                ret = menu_main(job)
                rep = ret
            else:
                rep = ''
        elif rep == '2':
            rep = i_want_to_register_to_the_application(job)

################################################################################
#
################################################################################

def main():
    #job = JobDb(host="localhost",user="cse",password="cseMysql1!",database="BogusModee")
    job = JobDb(host="mysqlhost",user="bogusmodee",password="BogusModee1!",database="BogusModee")
    job.open_db()
    menu_init(job)
    #job.display_version()
    #job.display_gamer()
    job.close_db()

if __name__ == '__main__':
    main()
