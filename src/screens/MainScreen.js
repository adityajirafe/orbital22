import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { NoTradeItem, TradeItem } from '../components';
import { compareTime } from '../firebase/dbhelper';
import { COLOURS } from '../styles/Colours';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const MainScreen = (props) => {
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

    return (
        <View style={globalStyles.container}>
            <View style={styles.trades}>
                <View style={styles.tradeListContainer}>
                    {trades.length == 0 ? (
                        <NoTradeItem style={styles.tradeList} />
                    ) : (
                        <FlatList
                            style={styles.tradeList}
                            data={trades.sort((a, b) =>
                                compareTime(a.time, b.time)
                            )}
                            renderItem={({ item, index }) => {
                                return (
                                    <TradeItem
                                        item={item}
                                        index={index}
                                        style={styles.tradeItem}
                                    />
                                );
                            }}
                        />
                    )}
                </View>
            </View>
            <StatusBar style="auto" />
        </View>
    );
};

export default MainScreen;

const styles = StyleSheet.create({
    tradeListContainer: {
        flex: 1,
        flexDirection: 'row',
        backgroundColor: COLOURS.secondary,
        marginTop: 20,
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        paddingHorizontal: 20,
        paddingVertical: 40,
    },
    tradeList: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
    },
    trades: {
        flex: 1,
    },
    tradeEntry: {
        padding: 20,
    },
    tradeItem: {
        borderRadius: 20,
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
