import check_update
import define_word


def startapp():
    # Start the key detection process
    define_word.start_key_detection()
    # Call the function to check for updates at the start of the app
    check_update.check_for_update()


if __name__ == "__main__":
    startapp()