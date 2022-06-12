import { signInWithEmailAndPassword } from 'firebase/auth';
import React, { useState } from 'react';
import {
    View,
    Text,
    Keyboard,
    KeyboardAvoidingView,
    Platform,
    Alert,
} from 'react-native';

import { AuthTextInput, AuthPressable, FeatureImage } from '../components';
import { auth } from '../firebase';
import { globalStyles } from '../styles/Styles';

const AuthScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const missingFieldsAlert = () => {
        Alert.alert('Missing fields, please try again!');
    };

    const userNotFoundAlert = () => {
        Alert.alert('Error: User not found');
    };

    const loginHandler = async () => {
        if (email.length === 0 || password.length < 6) {
            missingFieldsAlert();
            return;
        }

        await signInWithEmailAndPassword(auth, email, password)
            .then((userCredentials) => {
                const user = userCredentials.user;

                console.log(user);

                restoreForm();
            })
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;

                console.error('[loginHandler]', errorCode, errorMessage);
                if (errorCode == 'auth/user-not-found') {
                    userNotFoundAlert();
                }
            });
    };

    const restoreForm = () => {
        setEmail('');
        setPassword('');
        Keyboard.dismiss();
    };

    return (
        <KeyboardAvoidingView
            style={{ flex: 1 }}
            behavior={Platform.OS === 'ios' ? 'padding' : null}>
            <View style={globalStyles.container}>
                <FeatureImage />
                <View style={globalStyles.container_auth}>
                    <Text
                        style={[
                            globalStyles.welcomeText,
                            globalStyles.boldText,
                        ]}>
                        {`Log in to your CoinValet Account!`}
                    </Text>
                    <AuthTextInput
                        value={email}
                        placeholder="Your Email"
                        textHandler={setEmail}
                        keyboardType="email-address"
                    />
                    <AuthTextInput
                        value={password}
                        placeholder="Your Password"
                        textHandler={setPassword}
                        secureTextEntry
                    />
                    <AuthPressable
                        onPressHandler={loginHandler}
                        title={'LOG IN'}
                    />
                </View>
                <View style={globalStyles.blankContainer}></View>
            </View>
        </KeyboardAvoidingView>
    );
};

export default AuthScreen;
