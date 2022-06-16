import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { COLOURS } from '../styles/Colours';

import { METRICS } from '../data/portfolioMetrics';
import DashBoardItem from './DashBoardItem';

const DashBoard = () => {
    const {
        dailyProfit,
        ATProfit,
        todaysGain,
        totalGain,
        biggestWinner,
        biggestLoser,
    } = METRICS[0];

    return (
        <View style={styles.portfolioContainer}>
            <View style={styles.portfolio}>
                <DashBoardItem heading={'24h Profit'} text={dailyProfit} />
                <DashBoardItem heading={'All Time P&L'} text={ATProfit} />
                <DashBoardItem
                    heading={'Biggest Winner'}
                    text={biggestWinner}
                />
            </View>
            <View style={styles.portfolio}>
                <DashBoardItem heading={"Today's Gain"} text={todaysGain} />
                <DashBoardItem heading={'Platform Gain'} text={totalGain} />
                <DashBoardItem heading={'Biggest Loser'} text={biggestLoser} />
            </View>
        </View>
    );
};

export default DashBoard;

const styles = StyleSheet.create({
    portfolio: {
        flex: 1,
        flexDirection: 'row',
    },
    portfolioContainer: {
        flex: 1,
    },
});
