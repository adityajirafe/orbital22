import React, { useState, useEffect } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { StyleSheet, Text, View, FlatList, Pressable } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { fs } from '../firebase';
import DashBoardItem from './DashBoardItem';
import DashBoard from './DashBoard';
import { NoTradeItem, TradeItemFriend } from '../components';
import { compareTime } from '../firebase/dbhelper';
import { COLOURS } from '../styles/Colours';
import PositionList from './PositionList';

const FriendPortfolioCard = (props) => {
    const { email } = props;
    const heading = 'All Time PnL';
    const fsReference = 'all-time_PnL';
    const [metric, setMetric] = useState('');
    const [metricTitle, setMetricTitle] = useState('');
    const [positions, setPositions] = useState([]);
    const [trades, setTrades] = useState([]);
    const [isSending, setIsSending] = useState(false);
    const [empty, setEmpty] = useState(true);

    const prepare = async () => {
        const reference = email
            ? `UserPortfolio/${email}/`
            : 'UserPortfolio/adi/';
        const docRefMetrics = collection(fs, reference, 'metrics');
        getDocs(docRefMetrics).then((doc) => {
            doc.forEach((docu) => {
                let metric_data = docu.data();
                if (docu.id == fsReference) {
                    setMetric(metric_data.value);
                    setMetricTitle(metric_data.coin);
                }
            });
        });
        const positionReference = email
            ? `UserPortfolio/${email}/`
            : 'UserPortfolio/adi/';
        const docRef = collection(fs, positionReference, 'positions');
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let position = docu.data();
                // console.log('position', position);
                setPositions((positions) => [...positions, position]);
                // console.log(positions);
            });
        });
        const tradeReference = email
            ? `UserPortfolio/${email}/trades`
            : 'UserPortfolio/adi/trades';
        const tradeDocRef = collection(fs, tradeReference);
        await getDocs(tradeDocRef).then((doc) => {
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
        console.log('Refreshing');
        setIsSending(true);
        setPositions([]);
        setMetric('');
        setMetricTitle('');
        setTrades([]);
        prepare();
        wait(1000).then(() => setIsSending(false));
    };

    useEffect(() => {
        setIsSending(true);
        prepare();
        setIsSending(false);
    }, []);

    return (
        <View style={styles.mainContainer}>
            <View style={styles.topContainer}>
                <View style={styles.headerContainer}>
                    <View style={styles.headerBlank} />
                    <Pressable
                        title={'Refresh'}
                        disabled={isSending}
                        onPress={refresh}>
                        <Icon
                            name="refresh"
                            size={24}
                            style={{
                                color: COLOURS.black,
                                flex: 1,
                                marginTop: 2,
                            }}
                        />
                    </Pressable>
                </View>
                <View style={styles.metricContainer}>
                    <View style={styles.emailContainer}>
                        <View style={styles.titleContainer}>
                            <View style={styles.titleContainer2}>
                                <Text style={styles.title}>{email}</Text>
                            </View>
                        </View>
                    </View>
                    <View style={styles.metric}>
                        <DashBoardItem
                            heading={'All Time PnL'}
                            fsReference={'all-time_PnL'}
                            email={email}
                        />
                    </View>
                </View>
            </View>
            <View style={styles.positionContainer}>
                <View style={styles.componentHeader}>
                    <Text style={styles.title}>Positions</Text>
                </View>
                <PositionList positions={positions} />
            </View>
            <View style={styles.componentHeader2}>
                <Text style={styles.title}>Trade History</Text>
            </View>
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
                                <TradeItemFriend
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
    );
};

export default FriendPortfolioCard;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        marginTop: 2,
        borderRadius: 20,
        width: 340,
    },
    topContainer: {
        flex: 1,
        borderRadius: 20,
        borderWidth: 2,
        backgroundColor: COLOURS.lightGrey,
    },
    headerContainer: {
        flex: 1,
        flexDirection: 'row',
        // backgroundColor: COLOURS.black,
    },
    metricContainer: {
        flex: 4,
        flexDirection: 'row',
        margin: 10,
    },
    emailContainer: {
        flex: 1,
        flexDirection: 'column',
        marginRight: 10,
        marginVertical: 10,
    },
    expandButtonContainer: {
        flex: 1,
        justifyContent: 'center',
        backgroundColor: COLOURS.lightGrey,
        flex: 1,
        alignItems: 'center',
    },
    expandButton: {
        backgroundColor: COLOURS.green,
        borderRadius: 20,
        borderWidth: 1,
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        width: '70%',
        marginTop: 10,
        marginBottom: 30,
    },
    button: {
        fontFamily: 'roboto',
        fontSize: 10,
        color: COLOURS.black,
    },
    metric: {
        flex: 1,
        marginLeft: 10,
    },
    headerBlank: {
        flex: 0.9,
    },
    positionContainer: {
        flex: 1,
        marginRight: 20,
        marginLeft: 20,
    },
    rowBottom: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        borderLeftWidth: 2,
        borderBottomWidth: 2,
        borderRightWidth: 2,
    },
    componentHeader: {
        backgroundColor: COLOURS.background,
        padding: 4,
        borderRadius: 20,
        borderWidth: 2,
        marginVertical: 3,
        width: '100%',
        alignSelf: 'center',
    },
    componentHeader2: {
        backgroundColor: COLOURS.background,
        padding: 4,
        borderRadius: 20,
        borderWidth: 2,
        width: '90%',
        alignSelf: 'center',
        marginTop: 6,
    },
    heading: {
        fontFamily: 'roboto-bold',
        // fontSize: 18,
        flex: 1,
        textAlign: 'center',
    },
    text: {
        fontFamily: 'roboto',
        // fontSize: 15,
        flex: 1,
        textAlign: 'center',
    },
    green: {
        color: COLOURS.green,
    },
    tradeListContainer: {
        flex: 1,
        flexDirection: 'row',
        backgroundColor: COLOURS.secondary,
        marginTop: 20,
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        paddingHorizontal: 1,
        paddingVertical: 40,
    },
    tradeList: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        marginLeft: 20,
        marginRight: 20,
        marginTop: -53,
    },
    tradeItem: {
        borderRadius: 20,
    },
    titleContainer: {
        flex: 1,
        justifyContent: 'center',
    },
    titleContainer2: {
        backgroundColor: COLOURS.background,
        marginBottom: 15,
        borderRadius: 20,
        borderWidth: 2,
        flex: 1,
        justifyContent: 'center',
    },
    title: {
        fontFamily: 'roboto-bold',
        textAlign: 'center',
        fontSize: 14,
        // flex: 1,
    },
});
