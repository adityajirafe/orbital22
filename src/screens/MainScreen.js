import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import React from 'react';
import { globalStyles } from '../styles/Styles';
import { TRADES } from '../data/trades';
import { METRICS } from '../data/portfolioMetrics';

import { DashBoardItem, TradeItem } from '../components';

const MainScreen = () => {

    const {dailyProfit, ATProfit, todaysGain, totalGain, biggestWinner, biggestLoser} = METRICS[0]
    return (
        <View style = {globalStyles.container}>
            <View style = {styles.trades}>
                <Text style = {[globalStyles.welcomeText, styles.header]}>
                    Trade History
                </Text>
                <View style = {styles.tradeListContainer}>
                    <View style = {styles.tradeListBorderLeft}></View>
                    <FlatList
                        style = {styles.tradeList} 
                        data={ TRADES }
                        renderItem = {({ item, index }) => {
                            return (
                                <TradeItem 
                                    item = { item } 
                                    index = { index }
                                /> );
                        }}
                    />
                    <View style = {styles.tradeListBorderRight}></View>
                </View>
            </View>
            <View style = {styles.portfolioContainer}>
                <Text style = {[globalStyles.welcomeText, styles.header]}>
                    Dashboard
                </Text>
                <View style = {styles.portfolio}>
                    <DashBoardItem style = {styles.widget} heading = {"24h Profit"} text = {dailyProfit} />
                    <DashBoardItem style = {styles.widget} heading = {"All Time P&L"} text = {ATProfit} />
                    <DashBoardItem style = {styles.widget} heading = {"Biggest Winner"} text = {biggestWinner} />
                </View>
                <View style = {styles.portfolio}>
                    <DashBoardItem heading = {"Today's Gain"} text = {todaysGain} />
                    <DashBoardItem heading = {"Platform Gain"} text = {totalGain} />
                    <DashBoardItem heading = {"Biggest Loser"} text = {biggestLoser} />
                </View>
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
    tradeListContainer: {
        flex: 1,
        flexDirection: 'row'
    },
    tradeListBorderLeft: {
        flex: 0.05,
        backgroundColor: 'black',
        borderTopLeftRadius: 20,
        borderBottomLeftRadius: 20
    },
    tradeListBorderRight: {
        flex: 0.05,
        backgroundColor: 'black',
        borderTopRightRadius: 20,
        borderBottomRightRadius: 20
    },
    tradeList: {
        flex: 1,
    },
    trades: {
        flex: 1,
    },
    tradeEntry: {
        padding: 20,
    },
    portfolioContainer: {
        flex: 1,
    },
    portfolio: {
        flex: 1,
        flexDirection: 'row'
    },
    widget: {
        
    }
})