# Chatbot features

## Air filter analysis

Air filter analysis is a feature integrated thanks to Krishnamurthy Vikram.
It is based on a linear regression on specific air filter images.
Once provided with a control image, this feature is able to determine the wear level of the user's air filter.

## Icon recognition

Icon recognition is an image analysis feature using a CNN model developed using PyTorch.
When the user gives an icon image to the chatbot, it will make a prediction among several classes and give a short description.

*Note: there are only 4 classes for now to make predictions, it should be extended.*

## QSearch

It is the search engine feature developed using custom techniques.
It requires to compute sequence trees and topic terms to make a search.

## Sentiment analysis

This feature is the core of MyNissan's chatbot personality.
It allows the chatbot to analyze the user's queries and to adapt its behavior based on it.

*Note: for now, the sentiment is either considered positive, neutral or negative. It should be extended to more sentiments.*

## Voice Interaction

Voice interaction regroups 2 features : a text-to-speech system and a speech-to-text one.
Therefore, the customer is allowed to record his voice to send a message and he can also listen to the chatbot's answers.