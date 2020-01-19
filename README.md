# Cormorant
## Overview
Cormorant is an experimental pipeline to provide an alternative to standard recommendation systems.

## Discussion
Most recommendation systems, such as Spotify and Youtube, operate on a fairly simple priciple: if person A like Song 1 and Song 2, then if person B like Song 1, they have a chance of liking Song 2.  

Cormorant does not do this.  Instead, Cormorant will attempt to look at the spectrogram of various songs and determine patterns as to which songs I like, and which ones I do not.  Think of this is as an objective differentiaton instead of a subjective or comparative one.

## Phases
	1.  Viability - Spectrogram test and spider test for youtube.
	2.  Training the Autoencoder
	3.  Setting up data - songs I like, songs I don't.  Probably want an interface and some kind of backend - Mongo?
