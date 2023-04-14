# nyt-digits

This is a simple python script which solves the New York Times "digits" puzzle game that was in Beta as of 04/14/23

Input file must be named problems.txt and look like the following:

TargetNumber: Space Delimited List of Numbers

So for example:
59: 2 3 5 11 15 25

You can have as many problems as you want, and you can make a problem skipped by adding a # to the front of it.

The output is the original problem, followed by a single equation showing the solution, follwed by a list of equations which correspond to the steps required to solve the problem.

From the example problem above:

59: [2, 3, 5, 11, 15, 25]
(2 + (3 * (11 + ((15 + 25) / 5)))) = 59.0
15 + 25 = 40
40 / 5 = 8.0
11 + 8.0 = 19.0
3 * 19.0 = 57.0
2 + 57.0 = 59.0