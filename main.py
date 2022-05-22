import iob_variables


def main():
    import setup_bot
    iob_variables.iob.add_event_handler(setup_bot.test)
    setup_bot.unpin_job()
    print("Running...")
    iob_variables.iob.run_until_disconnected()


if __name__ == '__main__':
    main()
