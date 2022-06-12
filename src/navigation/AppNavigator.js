import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { Text, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from '../firebase';

import { HomeScreen, AuthScreen, MainScreen, SignupScreen } from '../screens';

import { globalStyles } from '../styles/Styles';

const Stack = createNativeStackNavigator();
const AuthStack = createNativeStackNavigator();

const AppNavigator = () => {
    const [isAuth, setIsAuth] = useState(false);
    const [user, setUser] = useState('adi');

    useEffect(() => {
        const unsubscribeAuthStateChanged = onAuthStateChanged(
            auth,
            (authenticatedUser) => {
                if (authenticatedUser) {
                    setIsAuth(true);
                    console.log('email is ' + authenticatedUser.email);
                    setUser(authenticatedUser.email);
                } else {
                    setIsAuth(false);
                    setUser('');
                }
            }
        );
        return () => unsubscribeAuthStateChanged();
    }, []);

    const logoutHandler = () => {
        signOut(auth).then(() => {
            setIsAuth(false);
        });
    };

    const LogoutIcon = () => (
        <TouchableOpacity onPress={logoutHandler}>
            <Text>Logout</Text>
        </TouchableOpacity>
    );

    const MainNavigator = () => (
        <Stack.Navigator initialRouteName="main">
            <Stack.Screen
                name="main"
                options={{
                    title: 'Cytpo Trading Made Fun & Easy',
                    headerStyle: { backgroundColor: '#c8dfe4' },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                }}
                component={HomeScreen}
            />
            <Stack.Screen
                name="signup"
                options={{
                    title: 'Signup',
                    headerStyle: { backgroundColor: '#c8dfe4' },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                }}
                component={SignupScreen}
            />
            <Stack.Screen
                name="auth"
                options={{
                    title: 'Login',
                    headerStyle: { backgroundColor: '#c8dfe4' },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                }}
                component={AuthScreen}
            />
        </Stack.Navigator>
    );

    const MainScreenWithUser = () => {
        return <MainScreen username={user} />;
    };

    const AuthMainNavigator = () => (
        <AuthStack.Navigator>
            <AuthStack.Screen
                name="login"
                options={{
                    title: 'CoinValet',
                    headerStyle: { backgroundColor: '#c8dfe4' },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                    headerRight: () => <LogoutIcon />,
                }}
                component={MainScreenWithUser}
            />
        </AuthStack.Navigator>
    );

    return (
        <NavigationContainer>
            {isAuth ? <AuthMainNavigator /> : <MainNavigator />}
            <StatusBar style="auto" />
        </NavigationContainer>
    );
};

export default AppNavigator;
