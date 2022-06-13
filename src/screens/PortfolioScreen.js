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
import { COLOURS } from '../styles/Colours';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const PortfolioScreen = (props) => {
    const { email } = props;
    const [trades, setTrades] = useState([]);
    useConstructor(() => {
        // console.log('Rendering screen now');
        // Demo Account contains empty trades while email loads
        const reference = email
            ? `UserPortfolio/${email}/trades`
            : 'UserPortfolio/adi/trades';
        const docRef = collection(fs, reference);
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let trade = docu.data();
                setTrades((trades) => [...trades, trade]);
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
    // console.log(trades);
    return (
        <View style={globalStyles.container}>
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

export default PortfolioScreen;

const styles = StyleSheet.create({
    header: {
        paddingTop: 20,
    },
    tradeListContainer: {
        flex: 1,
        flexDirection: 'row',
        backgroundColor: COLOURS.background,
    },
    tradeListBorderLeft: {
        flex: 0.05,
        backgroundColor: COLOURS.black,
        borderTopLeftRadius: 20,
        borderBottomLeftRadius: 20,
    },
    tradeListBorderRight: {
        flex: 0.05,
        backgroundColor: COLOURS.black,
        borderTopRightRadius: 20,
        borderBottomRightRadius: 20,
    },
    tradeList: {
        flex: 1,
        backgroundColor: COLOURS.background,
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
