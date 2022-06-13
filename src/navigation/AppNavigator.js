import 'react-native-gesture-handler';
import 'react-native-reanimated';
import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { Text, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { View } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from '../firebase';

import { HomeScreen, AuthScreen, MainScreen, SignupScreen } from '../screens';
import { CustomDrawerContent } from '../components';
import { createDrawerNavigator } from '@react-navigation/drawer';

import { globalStyles } from '../styles/Styles';
import CoinValetIcon from '../components/CoinValetIcon';
import { COLOURS } from '../styles/Colours';
import PortfolioScreen from '../screens/PortfolioScreen';

const Stack = createNativeStackNavigator();
const AuthStack = createNativeStackNavigator();
const Drawer = createDrawerNavigator();

const AppNavigator = () => {
    const [isAuth, setIsAuth] = useState(false);
    const [user, setUser] = useState('demo');

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
        <TouchableOpacity
            onPress={logoutHandler}
            style={globalStyles.logoutIcon}>
            <Text>Logout</Text>
        </TouchableOpacity>
    );

    const MainNavigator = () => (
        <Stack.Navigator initialRouteName="main">
            <Stack.Screen
                name="main"
                options={{
                    title: 'Cytpo Trading Made Fun & Easy',
                    headerStyle: { backgroundColor: COLOURS.background },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                }}
                component={HomeScreen}
            />
            <Stack.Screen
                name="signup"
                options={{
                    title: 'Signup',
                    headerStyle: { backgroundColor: COLOURS.background },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                }}
                component={SignupScreen}
            />
            <Stack.Screen
                name="auth"
                options={{
                    title: 'Login',
                    headerStyle: { backgroundColor: COLOURS.background },
                    headerTitleStyle: { fontFamily: 'roboto-bold' },
                }}
                component={AuthScreen}
            />
        </Stack.Navigator>
    );

    const MainScreenWithUser = () => {
        return <MainScreen email={user} />;
    };

    const PortfolioScreenWithUser = () => {
        return <PortfolioScreen email={user} />;
    };

    const DrawerNavigator = () => {
        return (
            <Drawer.Navigator
                screenOptions={{
                    headerShown: true,
                    drawerType: 'slide',
                    drawerStyle: {
                        width: 220,
                        backgroundColor: COLOURS.background,
                    },
                    // overlayColor: null, // to avoid the faded background

                    // to style labels inside drawer
                    drawerActiveTintColor: COLOURS.black,
                    drawerItemStyle: { backgroundColor: null },
                    drawerLabelStyle: {
                        fontFamily: 'roboto-bold',
                        fontSize: 15,
                    },
                }}
                drawerContent={(props) => <CustomDrawerContent {...props} />}>
                <Drawer.Screen
                    name="history"
                    options={{
                        title: 'Trade History',
                        headerStyle: { backgroundColor: COLOURS.background },
                        headerTitleStyle: { fontFamily: 'roboto-bold' },
                        headerRight: () => <LogoutIcon />,
                        drawerIcon: () => (
                            <Icon
                                name="clipboard-text-clock"
                                size={22}
                                style={{ marginRight: -20 }}
                            />
                        ),
                    }}>
                    {(props) => <MainScreenWithUser {...props} />}
                </Drawer.Screen>
                <Drawer.Screen
                    name="metrics"
                    options={{
                        title: 'Portfolio',
                        headerStyle: { backgroundColor: COLOURS.background },
                        headerTitleStyle: { fontFamily: 'roboto-bold' },
                        headerRight: () => <LogoutIcon />,
                        drawerIcon: () => (
                            <Icon
                                name="bitcoin"
                                size={22}
                                style={{ marginRight: -20 }}
                            />
                        ),
                    }}>
                    {(props) => <PortfolioScreenWithUser {...props} />}
                </Drawer.Screen>
            </Drawer.Navigator>
        );
    };

    // const AuthMainNavigator = () => (
    //     <AuthStack.Navigator>
    //         <AuthStack.Screen
    //             name="login"
    //             options={{
    //                 title: 'CoinValet',
    //                 headerStyle: { backgroundColor: COLOURS.background },
    //                 headerTitleStyle: { fontFamily: 'roboto-bold' },
    //                 headerRight: () => <LogoutIcon />,
    //             }}
    //             component={DrawerNavigator}
    //         />
    //     </AuthStack.Navigator>
    // );

    return (
        <NavigationContainer>
            {isAuth ? <DrawerNavigator /> : <MainNavigator />}
            <StatusBar style="auto" />
        </NavigationContainer>
    );
};

export default AppNavigator;
