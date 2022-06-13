import React from 'react';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { View } from 'react-native';

import { MainScreen } from '../screens';

const Drawer = createDrawerNavigator();

const MainScreenWithUser = () => {
    return <MainScreen username="adi" />;
};

const DrawerNavigator = () => {
    return (
        <Drawer.Navigator
            screenOptions={{
                headerShown: false,
                drawerType: 'slide',
                drawerStyle: {
                    width: 200,
                    backgroundColor: COLOURS.background,
                },
            }}>
            <Drawer.Screen name="trial" component={MainScreenWithUser} />
        </Drawer.Navigator>
    );
};

export default DrawerNavigator;
