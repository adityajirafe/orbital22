import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { globalStyles } from '../styles/Styles';

const Header = () => {
    return (
        <View style={globalStyles.header}>
            <Text style={globalStyles.title}> CoinValet</Text>
        </View>
    );
};
export default Header;
