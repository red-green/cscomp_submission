Computer science competition program submission server
-------

For a computer programming competition to simplify submitting programs.

To run it, first fo=ind the IP address of the computer. then run the server:

```
python main.py
```

This will start everything. Competitors will be able to simply type in the ip address at port 5000 and access the submission page. The judges will see a line when they start up the server like this:

```
Submission list can be viewed at /view/ABCDEFGH
```

This is the secret URL that can be used to view the submission list. You can change the string by changing the `SECRET` variable at the top of the main python file.

To access the submissions list then, assuming the IP address of the computer running the server is `192.168.1.10` you type:

```
192.168.1.10:5000/view/ABCDEFGH
```

In the list, there are links that open a page where one can copy code.
