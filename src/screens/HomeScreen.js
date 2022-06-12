import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import React from 'react';
import { globalStyles } from '../styles/Styles';
import { FeatureImage } from '../components';

const HomeScreen = ({ navigation }) => {
    return (
        <View style={globalStyles.container}>
            <FeatureImage />
            <View style={styles.login_container}>
                <TouchableOpacity onPress={() => navigation.navigate('auth')}>
                    <Text style={styles.button}>Login</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => navigation.navigate('signup')}>
                    <Text style={styles.button}>Signup</Text>
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
        // paddingTop: 40,
    },
    button: {
        textAlign: 'center',
        fontFamily: 'roboto-bold',
        fontSize: 32,
        borderColor: '#FEFFED',
        borderWidth: 10,
        backgroundColor: '#FEFFED',
        width: 200,
        borderRadius: 20
    },
    empty: {
        flex: 0.3,
    },
});

export default HomeScreen;
