# Explanation

The current model for the calculation of the remaining light intensity is a heavily simplified approach. 
At the start of my research I tried to implement a better model. It didn't work. The problem is, that there are no reliable corresponding sources which have formulas explained and formulas that are applicable for our cause. 
Since we need to calculate the remaining light intensity from the bottom to the top of the atmosphere (or a given height within the atmosphere) and all three of us didn't study atmospheric physics we needed to find good reliable sources which give a step by step guide (or something similar) on how a calculation like this is done. The amount of relevant sources were close to zero.
I tried implementing a few approaches (as you can see in fabian_lightIntensity.py) and realized most of them do not work. 

The reason why there are so many sources in the Sources.txt is, because I have read them all and tried to derive a working model from the formulas which are used in these sources.

After a few attempts we asked a physicist from the university of Heidelberg if he can give us a hint on what I am doing wrong and how to build a working model. The only answer he gave us were the two PDF Files (Radiative_Transfer) which use some formulas I had already tried and some new ones. The Files did not contain every information I needed to build a working model, because some functions weren't explained and/or defined. I still tried to implement these formulas (Second try in the code) but it still wasn't returning correct values. 

We then settled to use a much more simplified model of the atmosphere and approximated the remaining light intensity at a given height using this model. 

The reason why I wrote this readme is, because I wanted to show how much research went into the calculations I did and to explain why there are so many sources and papers for such a simplified approach.

If you have any idea of why my models did not work or what I did wrong when calculating the remaining intensity, I would appreciate if you could explain it to me, because I'd like to correct it and have a working more complex model for our project. 

~Fabian
