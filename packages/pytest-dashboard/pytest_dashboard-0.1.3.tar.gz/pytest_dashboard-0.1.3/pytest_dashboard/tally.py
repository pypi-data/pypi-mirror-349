import fire

from pytest_dashboard._tally_progresses import monitor_progress

def main():
    fire.Fire(monitor_progress)

if __name__ =='__main__':
    main()
    
