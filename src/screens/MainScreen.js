import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';
import { TRADES } from '../data/trades';
import { METRICS } from '../data/portfolioMetrics';

import { DashBoardItem, NoTradeItem, TradeItem } from '../components';
import { addDummyData } from '../firebase/dbhelper';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const MainScreen = (props) => {
    const { username } = props;
    const [trades, setTrades] = useState([]);
    // console.log(username);
    useConstructor(() => {
        // console.log('Rendering screen now');
        const docRef = collection(fs, 'UserPortfolio/tom/trades');
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let trade = docu.data();
                console.log(trade);
                setTrades((trades) => [...trades, trade]);
                console.log(trades);
            });
        });
    });

    const {
        dailyProfit,
        ATProfit,
        todaysGain,
        totalGain,
        biggestWinner,
        biggestLoser,
    } = METRICS[0];
    console.log(trades);
    return (
        <View style={globalStyles.container}>
            <View style={styles.trades}>
                <Text style={[globalStyles.welcomeText, styles.header]}>
                    {username}
                </Text>
                <View style={styles.tradeListContainer}>
                    <View style={styles.tradeListBorderLeft}></View>
                    {trades.length == 0 ? (
                        <NoTradeItem />
                    ) : (
                        <FlatList
                            style={styles.tradeList}
                            data={trades}
                            renderItem={({ item, index }) => {
                                return <TradeItem item={item} index={index} />;
                            }}
                        />
                    )}
                    <View style={styles.tradeListBorderRight}></View>
                </View>
            </View>
            <View style={styles.portfolioContainer}>
                <Text style={[globalStyles.welcomeText, styles.header]}>
                    Dashboard
                </Text>
                <View style={styles.portfolio}>
                    <DashBoardItem
                        style={styles.widget}
                        heading={'24h Profit'}
                        text={dailyProfit}
                    />
                    <DashBoardItem
                        style={styles.widget}
                        heading={'All Time P&L'}
                        text={ATProfit}
                    />
                    <DashBoardItem
                        style={styles.widget}
                        heading={'Biggest Winner'}
                        text={biggestWinner}
                    />
                </View>
                <View style={styles.portfolio}>
                    <DashBoardItem heading={"Today's Gain"} text={todaysGain} />
                    <DashBoardItem heading={'Platform Gain'} text={totalGain} />
                    <DashBoardItem
                        heading={'Biggest Loser'}
                        text={biggestLoser}
                    />
                </View>
            </View>
            <StatusBar style="auto" />
        </View>
    );
};

export default MainScreen;

const styles = StyleSheet.create({
    header: {
        paddingTop: 20,
    },
    tradeListContainer: {
        flex: 1,
        flexDirection: 'row',
    },
    tradeListBorderLeft: {
        flex: 0.05,
        backgroundColor: 'black',
        borderTopLeftRadius: 20,
        borderBottomLeftRadius: 20,
    },
    tradeListBorderRight: {
        flex: 0.05,
        backgroundColor: 'black',
        borderTopRightRadius: 20,
        borderBottomRightRadius: 20,
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
        flexDirection: 'row',
    },
    widget: {},
});
