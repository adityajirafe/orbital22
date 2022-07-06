import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';
import { StyleSheet, Text, View, FlatList } from 'react-native';
import { COLOURS } from '../styles/Colours';
import FriendReqItem from './FriendReqItem';

const FriendReqList = (props) => {
    const { requests, email } = props;
    return (
        <View style={styles.mainContainer}>
            <FlatList
                data={requests}
                renderItem={({ item, index }) => {
                    return (
                        <FriendReqItem
                            item={item}
                            index={index}
                            email={email}
                        />
                    );
                }}
            />
        </View>
    );
};

export default FriendReqList;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
    },
});
