def filter_out3(data_dir):
    speed_path = os.path.join(data_dir,"speed.txt")

    with open(speed_path) as speed:
        speed_info = speed.readlines()

    # Create raw
    save = os.path.join(data_dir, 'speed_filtered.txt')
    position = open(save, 'w+')

    for i in range(len(speed_info)):
        speed_read = speed_info[i].strip().split()
        frame = speed_read[0]
        position.write(frame)
        position.write("\n")
    position.close()

    # Process for the replaced file
    speed2_path = os.path.join(data_dir,"speed_filtered.txt")

    with open(speed2_path, "r+") as speeds:
        speed2_info = speeds.readlines()


    # Scan oll of the object ID
    list_obj = []
    for i in range(len(speed_info)):
        speed_read = speed_info[i].strip().split()

        each_obj_speed = speed_read[1:]
        object_id = each_obj_speed[::2]
        object_speed = each_obj_speed[1::2]

        for j in range(len(object_id)):
            objek = object_id[j]
            list_obj.append(objek)

        list_obj = list(dict.fromkeys(list_obj))

    print("list_obj = ", list_obj)

    # Save the speed in a list
    # First scan over the object
    for aw in range(len(list_obj)):
        speed_temp = []
        frame_temp = []
        query_temp = []
        beda_temp = []
        bedap_temp = []
        bedan_temp = []

        # Scan over the speed.txt
        for j in range(len(speed_info)):
            speed_read = speed_info[j].strip().split()

            frame = speed_read[0]
            each_obj_speed = speed_read[1:]
            object_id = each_obj_speed[::2]
            object_speed = each_obj_speed[1::2]

            # Scan over the each frame
            for k in range(len(object_id)):
                objek = object_id[k]
                kecepatan = object_speed[k]

                # Kalo sama save di suatu list
                if objek == list_obj[aw]:
                    speed_temp.append(float(kecepatan))
                    frame_temp.append(frame)
                    query_temp.append(j)

        # speed_temp = data untuk diolah
        # query_temp = buat posisi frame

        # Filtered out
        total_data = len(speed_temp)
        temporary_place = []
        temporary_place.append(speed_temp[0])
        temporary_place.append(speed_temp[0])

        # Print object ID
        print("Objek = ", list_obj[aw])

        # Get the average
        # To set the threshold
        for i in range(2,total_data):
            now = speed_temp[i]

            if i == 2:
                past_check = speed_temp[i-1]
            else:
                past_check = speed_temp[i-1]

            beda_temp.append(abs(past_check - now))

            beda_c = abs(past_check - now)
            check_c = now - past_check

            if check_c >= 0:
                bedap_temp.append(beda_c)
            else:
                bedan_temp.append(beda_c)

        #print("bedap_temp = ", bedap_temp)
        #print("panjang p 1 = ", len(bedap_temp))
        #print("bedan_temp = ", bedan_temp)
        #print("panjang n 1 = ", len(bedan_temp))

        # print("rata1 + = ", mean(bedap_temp))
        # print("rata1 - = ", mean(bedan_temp))

        # Remove the outlier
        # Increase
        if len(bedap_temp) > 1:
            rata2 = mean(bedap_temp)
            std_d = np.std(bedap_temp)
            sigma_atas = 0.7
            sigma_bawah = 2
            atas = rata2 + (std_d * sigma_atas)
            bawah = rata2 - (std_d * sigma_bawah)

            # Remove outlier
            bedap_temp = [x for x in bedap_temp if x > bawah]
            bedap_temp = [x for x in bedap_temp if x < atas]

            if len(bedap_temp) >= 1:
                # Set the threshold
                rata2 = mean(bedap_temp)
                threhold_low = rata2*0.25
                threshold_high = rata2*0.5
            else:
                threhold_low = 5
                threshold_high = 12

        elif len(bedap_temp) <= 1:
            threhold_low = 5
            threshold_high = 12
        else:
            threhold_low = 5
            threshold_high = 12

        # Decrease
        if len(bedan_temp) > 1:
            rata2 = mean(bedan_temp)
            std_d = np.std(bedan_temp)
            sigma_atas = 1
            sigma_bawah = 2
            atas = rata2 + (std_d * sigma_atas)
            bawah = rata2 - (std_d * sigma_bawah)

            # Remove outlier
            bedan_temp = [x for x in bedan_temp if x > bawah]
            bedan_temp = [x for x in bedan_temp if x < atas]

            if len(bedan_temp) >= 1:
                # Set the threshold
                rata2 = mean(bedan_temp)
                threhold_low_n = rata2*0.33
                threshold_high_n = rata2*0.66
            else:
                threhold_low_n = 5
                threshold_high_n = 12

        elif len(bedan_temp) <= 1:
            threhold_low = 5
            threshold_high = 12
        else:
            threhold_low_n = 5
            threshold_high_n = 12

        # print("rata2 + = ", mean(bedap_temp))
        # print("rata1 - = ", mean(bedan_temp))
        # print("panjang p 2 = ", len(bedap_temp))
        # print("panjang n 2 = ", len(bedan_temp))
        # print("bedap_temp = ", bedap_temp)
        # print("rata2 = ", rata2)
        # print("threhold_low = ", threhold_low)
        # print("threshold_high = ", threshold_high)
        #print("threhold_low_n = ", threhold_low_n)

        # Filtered out based on the threshold
        for i in range(2,total_data):
            now = speed_temp[i]

            if i == 2:
                past = speed_temp[i-1]
            else:
                past = sekarang

            beda = abs(past - now)
            check_con = now - past

            if check_con >= 0:
                positive = True
            else:
                positive = False

            # Bawah 10 pake threshold awal
            if i <= 10:
                tp_low = 40
                tp_high = 50
                tn_low = 40
                tn_high = 50
            else:
                tp_low = threhold_low
                tp_high = threshold_high
                tn_low = threhold_low_n
                tn_high = threshold_high_n

            if positive == True:
                if tp_low < beda <= tp_high:
                    adder = beda/2
                    temporary_place.append(past+adder)
                    sekarang = past+adder
                elif beda > tp_high:
                    temporary_place.append(past)
                    sekarang = past
                else:
                    temporary_place.append(now)
                    sekarang = now
            else:
                if tn_low < beda <= tn_high:
                    adder = beda/3
                    temporary_place.append(past-adder)
                    sekarang = past-adder
                elif beda > tn_high:
                    adder = beda/2
                    temporary_place.append(past-adder)
                    sekarang = past
                elif beda > 50:
                    adder = beda*0.75
                    temporary_place.append(past-adder)
                    sekarang = past-adder

                else:
                    temporary_place.append(now)
                    sekarang = now

        print("bedap_temp = ", bedap_temp)
        print("temporary_place = ", temporary_place)

        plt.plot(range(len(temporary_place)), temporary_place, label = 'EMA')
        plt.title('EMA Speed ' + str(list_obj[aw]))
        plt.xlabel('Frame')
        plt.ylabel('Speed')
        plt.legend()
        plt.show()

        predictions = calculate_kalman(temporary_place)

        plt.plot(range(len(predictions)), predictions, label = 'Kalman')
        plt.title('Kalman Speed ' + str(list_obj[aw]))
        plt.xlabel('Frame')
        plt.ylabel('Speed')
        plt.legend()
        plt.show()

        id_now = list_obj[aw]

        speed2_path = os.path.join(data_dir,"speed_filtered.txt")
        speeds = open(speed2_path, 'r+')
        speed2_info = speeds.readlines()

        print("")
        print("objek = ", list_obj[aw])
        print("speed_temp = ", speed_temp)
        print("predictions = ", predictions)
        print("")
        print("")


        for x in range(len(speed2_info)):
            timpa = speed2_info[x].strip()
            tag = False
            #print("timpa = ", timpa)

            for y in range(len(query_temp)):
                urutan = query_temp[y]
                speed_now = predictions[y]

                # print("x = ", x, "  y = ", y)
                # print("urutan = ", urutan)

                if x == urutan:
                    tag = True
                    kec = speed_now[0]
                    #print("speed_now = ", speed_now[0])
                    baru_tulis = timpa + " " + str(id_now) + " " + str(kec)
                    speeds.write(baru_tulis)
                    
            if tag == False:
                speeds.write(timpa)

            speeds.write("\n")

        speeds.close()

        # Take only the new
        n = len(speed2_info)
        nfirstlines = []

        with open(speed2_path) as f, open(os.path.join(data_dir,"bigfiletmp.txt"), "w") as out:
            for x in range(n):
                nfirstlines.append(next(f))
            for line in f:
                out.write(line)

        # NB : it seems that `os.rename()` complains on some systems
        # if the destination file already exists.
        os.remove(speed2_path)
        os.rename(os.path.join(data_dir,"bigfiletmp.txt"), speed2_path)



if __name__ == '__main__' :
    data_dir = "/media/ferdyan/LocalDiskE/Hasil/dataset/Final2/10/"
    #read_speed(data_dir, intersec = True)
    #filter_speed(data_dir)
    #filter_speed2(data_dir)
    #filter_speed3(data_dir)
    # intersec = False
    # draw(data_dir, intersec = True)
    #banding(data_dir)

    # filter_out(data_dir)
    # filter_speed(data_dir)
    # filter_speed2(data_dir)
    # banding2(data_dir)

    # Compute mean
    #filter_out2(data_dir)

    # Compute mean & std, remove outlier
    filter_out3(data_dir)
