import {
    DrawerContentScrollView,
    DrawerItemList,
} from '@react-navigation/drawer';
import { View } from 'react-native';

import CoinValetIcon from './CoinValetIcon';

const CustomDrawerContent = (props) => {
    return (
        <DrawerContentScrollView style={{ paddingVertical: 30 }}>
            <View style={{ marginLeft: 20, marginVertical: 40 }}>
                <CoinValetIcon />
            </View>
            <DrawerItemList {...props} />
        </DrawerContentScrollView>
    );
};

export default CustomDrawerContent;
