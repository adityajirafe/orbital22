import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import React from 'react';
import { globalStyles } from '../styles/Styles';

const LoginScreen = () => {
    return (
        <View style = {globalStyles.container}>
            <Text>Hello</Text>
            <StatusBar style="auto" />
        </View>
    )
}

export default LoginScreen