%% Group 66 assignment 1 Matlab
clear all
close all

% Imported files
input_features = importdata('features.txt')';
targets = ind2vec(importdata('targets.txt')');

% Matlab toolbox functions
hiddenneurons = patternnet(30);
[hiddenneurons,mse] = train(hiddenneurons,input_features,targets);
view(hiddenneurons);
output_of_MLP = hiddenneurons(input_features);

% Plotting confusion plot
figure
plotconfusion(targets,output_of_MLP)

% Plotting performance plot
figure
plotperform(mse)
title('')
xlabel('Number of epochs')
ylabel('MSE')
