import { StatusBar } from 'expo-status-bar';
import {
    View,
    Text,
    StyleSheet,
    FlatList,
    Button,
    Pressable,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import React, { useState, useEffect } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { DashBoard, PositionList } from '../components';
import { COLOURS } from '../styles/Colours';

const PortfolioScreen = (props) => {
    const { email } = props;
    const [positions, setPositions] = useState([]);
    const [isSending, setIsSending] = useState(false);

    const prepare = async () => {
        const reference = email
            ? `UserPortfolio/${email}/`
            : 'UserPortfolio/adi/';
        const docRef = collection(fs, reference, 'positions');
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let position = docu.data();
                // console.log('position', position);
                setPositions((positions) => [...positions, position]);
                // console.log(positions);
            });
        });
    };

    const wait = (timeout) => {
        return new Promise((resolve) => setTimeout(resolve, timeout));
    };

    const refresh = () => {
        setIsSending(true);
        setPositions([]);
        prepare();
        wait(1000).then(() => setIsSending(false));
    };

    useEffect(() => {
        setIsSending(true);
        prepare();
        setIsSending(false);
    }, []);

    return (
        <View style={globalStyles.container}>
            <View style={styles.portfolioContainer}>
                <View style={styles.headerContainer}>
                    <View style={styles.titleContainer}>
                        <Text style={styles.title}>Current positions</Text>
                    </View>
                    <Pressable
                        title={'Refresh'}
                        disabled={isSending}
                        onPress={refresh}>
                        <Icon
                            name="refresh"
                            size={30}
                            style={{
                                color: COLOURS.white,
                                marginTop: 12,
                                marginLeft: 10,
                            }}
                        />
                    </Pressable>
                </View>
                <View style={styles.positionList}>
                    <PositionList positions={positions} />
                </View>
                <View style={styles.dashboardContainer}>
                    <View style={styles.titleContainer2}>
                        <Text style={styles.title}>Performance</Text>
                    </View>
                    <DashBoard email={email} />
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
    headerContainer: {
        flexDirection: 'row',
    },
    portfolioContainer: {
        flex: 1,
        marginTop: 20,
        backgroundColor: COLOURS.secondary,
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        paddingHorizontal: 20,
        paddingVertical: 40,
    },
    positionList: {
        flex: 1,
        paddingBottom: 20,
    },
    dashboardContainer: {
        flex: 1.5,
    },
    titleContainer: {
        backgroundColor: COLOURS.background,
        padding: 15,
        marginBottom: 20,
        borderRadius: 20,
        borderWidth: 2,
        flex: 1,
    },
    titleContainer2: {
        backgroundColor: COLOURS.background,
        padding: 15,
        marginBottom: 20,
        borderRadius: 20,
        borderWidth: 2,
    },
    title: {
        fontFamily: 'roboto-bold',
        textAlign: 'center',
        fontSize: 16,
    },
});
