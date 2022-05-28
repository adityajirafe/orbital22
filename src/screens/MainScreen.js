import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import React, { useState } from 'react';
import { globalStyles } from '../styles/Styles';
import { TRADES } from '../data/trades';

import { TradeItem } from '../components';

const MainScreen = () => {

    return (
        <View style = {globalStyles.container}>
            <View style = {styles.trades}>
                <Text style = {[globalStyles.welcomeText, styles.header]}>
                    Trade History
                </Text>
                <FlatList 
                    data={ TRADES }
                    renderItem = {({ item, index }) => {
                        return (
                            <TradeItem 
                                item = { item } 
                                index = { index }
                            /> );
                    }}
                />
            </View>
            <View style = {styles.portfolio}>

            </View>
            <StatusBar style="auto" /> 
        </View>
    );
}

export default MainScreen

const styles = StyleSheet.create({
    header: {
        paddingTop: 20
    },
    trades: {
        flex: 1,
    },
    tradeEntry: {
        padding: 20,
    },
    portfolio: {
        flex: 1,
    }
})