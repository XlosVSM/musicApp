from spleeter.separator import Separator

if __name__ == "__main__":
    separator = Separator('spleeter:5stems')
    separator.separate_to_file('./BlackParade.wav', './output')