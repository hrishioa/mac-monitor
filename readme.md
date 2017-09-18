# Mac-Monitor

Simple application to monitor and log the vitals of a MacBook. Built with bad code and a day of frustration about the new 13-inch Macbook Pro with Touch Bar(tm)'s battery life.



## How to Use

1. Install the required dependencies.

   1. ```shell
      sudo gem install iStats
      ```

   2. ```shell
      brew install brightness
      ```

   3. ```shell
      brew install pcre
      ```

   4. ```shell
      pip install crontab
      ```

2. Test using a complete path to a log-file of your choice.

```shell
python main.py /Users/.../test.csv
```

3. Once it works, activate the crontab to log for a desired number of minutes

```shell
python main.py <full filename for logfile> --cron-set <number of minutes>
```

If `launchd` is preferred, there is also a sample plist file included.

Enjoy!
