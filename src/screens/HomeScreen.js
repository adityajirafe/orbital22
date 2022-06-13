import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import React from 'react';
import { globalStyles } from '../styles/Styles';
import { FeatureImage } from '../components';
import { COLOURS } from '../styles/Colours';

const HomeScreen = ({ navigation }) => {
    return (
        <View style={globalStyles.container}>
            <FeatureImage />
            <View style={styles.login_container}>
                <TouchableOpacity
                    onPress={() => navigation.navigate('auth')}
                    style={styles.button}>
                    <Text style={styles.buttonText}>Login</Text>
                </TouchableOpacity>
                <TouchableOpacity
                    onPress={() => navigation.navigate('signup')}
                    style={styles.button}>
                    <Text style={styles.buttonText}>Register</Text>
                </TouchableOpacity>
            </View>
            <View style={styles.empty}></View>
            <StatusBar style="auto" />
        </View>
    );
};

const styles = StyleSheet.create({
    image: {
        width: '100%',
        height: '100%',
        resizeMode: 'contain',
    },
    image_container: {
        flex: 1,
    },
    login_container: {
        flex: 1,
        justifyContent: 'space-evenly',
        alignItems: 'center',
    },
    button: {
        borderRadius: 20,
        backgroundColor: COLOURS.secondary,
    },
    buttonText: {
        textAlign: 'center',
        fontFamily: 'roboto-bold',
        fontSize: 30,
        borderWidth: 2,
        width: 200,
        height: 50,
        borderRadius: 20,
        color: COLOURS.darkGrey,
    },
    empty: {
        flex: 0.3,
    },
});

export default HomeScreen;
