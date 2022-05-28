import {
    View,
    Text,
    Keyboard,
    KeyboardAvoidingView,
    Platform,
    Alert
} from 'react-native';
import React, { useState } from 'react';
import {
    createUserWithEmailAndPassword
} from 'firebase/auth';

import { AuthTextInput, AuthPressable, FeatureImage } from '../components';
import { globalStyles } from '../styles/Styles';
import { auth } from '../firebase';

const SignupScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const signUpAlert = () => {
        Alert.alert(
            'Sign Up successfully completed!',
        );
    };

    const missingFieldsAlert = () => {
        Alert.alert(
            'Missing fields, please try again!',
        );
    };

    const userExistsAlert = () => {
        Alert.alert(
            'User already exists, please try again!'
        )
    }

    const signUpHandler = async () => {
        if (email.length === 0 || password.length < 6) {
            missingFieldsAlert();
            return;
        }

        try {
            const userCredentials = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredentials.user;

            // To show the user object returned
            console.log(user);

            restoreForm();
            signUpAlert();
        } catch (error) {
            const errorCode = error.code;
            const errorMessage = error.message;

            console.error('[signUpHandler]', errorCode, errorMessage);
            if (errorCode == 'auth/email-already-in-use') {
                userExistsAlert();
            }
        }
    };

    const restoreForm = () => {
        setEmail('');
        setPassword('');
        Keyboard.dismiss();
    };

    return (
        <KeyboardAvoidingView
            style={{ flex: 1 }}
            behavior={Platform.OS === 'ios' ? 'padding' : null}
        >
            <View style = {globalStyles.container}>
                <FeatureImage />
                <View style={globalStyles.container_auth}>
                    <Text style={[globalStyles.welcomeText, globalStyles.boldText]}>
                        {`Sign up for your CoinValet Account!`}
                    </Text>
                    <AuthTextInput
                        value={email}
                        placeholder='Your Email'
                        textHandler={setEmail}
                        keyboardType='email-address'
                    />
                    <AuthTextInput
                        value={password}
                        placeholder='Your Password'
                        textHandler={setPassword}
                        secureTextEntry
                    />
                    <AuthPressable
                        onPressHandler={signUpHandler}
                        title={'SIGN UP'}
                    />
                </View>
                <View style ={globalStyles.container}></View>
            </View>
        </KeyboardAvoidingView>
    );
};

export default SignupScreen;

