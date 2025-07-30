ver = "0.3.1"
bver = "alpha"
mod = ["music","log","flush","option"]
class option:
    def show_options():
        print("In LTPpyTools option,you can use this:")
        print("----SHOW----")
        print("show_this_ver():show ver")
        print("show_big_ver():look it alpha,beta,or build")
        print("show_mod():show mod")
        print("----SETTING----")
    


    def show_this_ver():
            print({ver})


    def show_big_ver():
        print({bver})

    def show_mod():
        print(*mod)



