class Observer:
    def update(*args, **kwargs):
        print(args)

        text_file = open("mail.txt", "w")
        text_file.write(str(args[0]))
        text_file.write(" ")
        text_file.write(str(args[1]))
        text_file.close()