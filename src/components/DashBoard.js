import React from 'react';
import { StyleSheet, View } from 'react-native';

import DashBoardItem from './DashBoardItem';

const DashBoard = (props) => {
    const { email } = props;

    return (
        <View style={styles.portfolioContainer}>
            <View style={styles.portfolio}>
                <DashBoardItem
                    heading={'Daily PnL'}
                    fsReference={'daily_PnL'}
                    email={email}
                />
                <DashBoardItem
                    heading={'All Time PnL'}
                    fsReference={'all-time_PnL'}
                    email={email}
                />
                <DashBoardItem
                    heading={'Best Position'}
                    fsReference={'best_position'}
                    email={email}
                />
            </View>
            <View style={styles.portfolio}>
                <DashBoardItem
                    heading={"Today's Gain"}
                    fsReference={'daily_PnL_percentage'}
                    email={email}
                />
                <DashBoardItem
                    heading={'Platform Gain'}
                    fsReference={'all-time_PnL_percentage'}
                    email={email}
                />
                <DashBoardItem
                    heading={'Worst Position'}
                    fsReference={'worst_position'}
                    email={email}
                />
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
