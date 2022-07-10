import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, FlatList, Button } from 'react-native';
import React, { useState, useEffect } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { NoTradeItem, TradeItem } from '../components';
import { compareTime } from '../firebase/dbhelper';
import { COLOURS } from '../styles/Colours';

const MainScreen = (props) => {
    const { email } = props;
    const [trades, setTrades] = useState([]);
    const [isSending, setIsSending] = useState(false);
    const [empty, setEmpty] = useState(true);

    const prepare = async () => {
        const reference = email
            ? `UserPortfolio/${email}/trades`
            : 'UserPortfolio/adi/trades';
        const docRef = collection(fs, reference);
        await getDocs(docRef).then((doc) => {
            setEmpty(false);
            doc.forEach((docu) => {
                // console.log(docu.data());
                let trade = docu.data();
                setTrades((trades) => [...trades, trade]);
            });
        });
    };

    const wait = (timeout) => {
        return new Promise((resolve) => setTimeout(resolve, timeout));
    };

    const refresh = () => {
        setIsSending(true);
        setTrades([]);
        prepare();
        wait(2000).then(() => setIsSending(false));
    };

    useEffect(() => {
        setIsSending(true);
        prepare();
        setIsSending(false);
    }, []);

    return (
        <View style={globalStyles.container}>
            <View style={styles.tradeListContainer}>
                {empty == true ? (
                    <NoTradeItem style={styles.tradeList} />
                ) : (
                    <FlatList
                        style={styles.tradeList}
                        data={trades.sort((a, b) =>
                            compareTime(a.time, b.time)
                        )}
                        onRefresh={refresh}
                        refreshing={isSending}
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
});
