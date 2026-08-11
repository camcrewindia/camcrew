import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Alert, TouchableOpacity } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { escrowService, EscrowDepositRecord } from '../../services/escrowService';
import { Package, Download, ShieldCheck, RefreshCw, CheckCircle2, Clock } from 'lucide-react-native';

export const OrderDetailScreen: React.FC<{ navigation: any; route: any }> = ({ navigation, route }) => {
  const { colors } = useTheme();
  const orderId = route?.params?.orderId || route?.params?.id || 'ORD-8921';

  const [escrow, setEscrow] = useState<EscrowDepositRecord | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEscrowStatus();
  }, []);

  const loadEscrowStatus = async () => {
    const records = await escrowService.getEscrowRecords();
    const found = records.find(r => r.orderId === orderId);
    if (found) {
      setEscrow(found);
    } else {
      // Default deposit record for preview
      setEscrow({
        orderId,
        depositAmount: 5000,
        status: 'held_in_escrow',
        heldAt: new Date().toISOString(),
      });
    }
  };

  const handleReturnEquipment = async () => {
    setLoading(true);
    try {
      const updated = await escrowService.markReturnedAndScheduleRefund(orderId);
      setEscrow(updated);
      Alert.alert(
        'Gear Return Verified! 📦',
        'Equipment inspection logged as passed. Your ₹5,000 security deposit refund has been scheduled (Auto-refund within 24 Hours).'
      );
    } catch (e) {
      Alert.alert('Error', 'Could not process return.');
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerInstantRefund = async () => {
    setLoading(true);
    try {
      const updated = await escrowService.processRefundNow(orderId);
      setEscrow(updated);
      Alert.alert('Deposit Refunded! 💰', `₹5,000 returned to your original payment method. Tx ID: ${updated.refundTxId}`);
    } catch (e) {
      Alert.alert('Error', 'Could not process refund.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={[styles.container, { backgroundColor: colors.background }]} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: colors.textPrimary }]}>Order & Escrow Details</Text>
        <Text style={[styles.orderId, { color: colors.accent }]}>{orderId}</Text>
      </View>

      {/* Shipment Status Card */}
      <Card style={styles.card}>
        <View style={styles.statusRow}>
          <Package size={24} color={colors.accent} />
          <View style={styles.statusMeta}>
            <Text style={[styles.statusTitle, { color: colors.textPrimary }]}>Order Status: Confirmed</Text>
            <Text style={[styles.statusSub, { color: colors.textFaint }]}>Delivery via Camcrew Logistics Express</Text>
          </View>
          <Badge label="Active Order" variant="info" />
        </View>
      </Card>

      {/* Security Deposit Escrow Tracker */}
      {escrow && (
        <Card style={[styles.card, { borderColor: colors.accent, borderWidth: 1 }]}>
          <View style={styles.escrowHeader}>
            <ShieldCheck size={22} color={colors.accent} />
            <Text style={[styles.escrowTitle, { color: colors.textPrimary }]}>
              Automated Rental Escrow Deposit
            </Text>
          </View>

          <View style={styles.escrowRow}>
            <Text style={[styles.escrowLabel, { color: colors.textSecondary }]}>Security Deposit Amount:</Text>
            <Text style={[styles.escrowValue, { color: colors.accent }]}>₹{escrow.depositAmount.toLocaleString()}</Text>
          </View>

          <View style={styles.escrowRow}>
            <Text style={[styles.escrowLabel, { color: colors.textSecondary }]}>Escrow Status:</Text>
            {escrow.status === 'held_in_escrow' ? (
              <Badge label="Held Safely in Escrow" variant="warning" />
            ) : escrow.status === 'refund_scheduled' ? (
              <Badge label="24-Hr Auto-Refund Scheduled" variant="info" />
            ) : (
              <Badge label="Deposit Refunded" variant="success" />
            )}
          </View>

          {escrow.status === 'held_in_escrow' ? (
            <Button
              title="Return Rental Gear (Start Inspection)"
              variant="secondary"
              size="md"
              loading={loading}
              icon={<RefreshCw size={16} color={colors.textPrimary} />}
              onPress={handleReturnEquipment}
              style={{ marginTop: 12 }}
            />
          ) : escrow.status === 'refund_scheduled' ? (
            <View style={{ marginTop: 12 }}>
              <Text style={[styles.refundNote, { color: colors.success }]}>
                ✓ Inspection Passed! Refund auto-executes within 24 Hours.
              </Text>
              <Button
                title="Instant Escrow Refund Now"
                variant="primary"
                size="md"
                loading={loading}
                icon={<CheckCircle2 size={16} color="#000000" />}
                onPress={handleTriggerInstantRefund}
                style={{ marginTop: 8 }}
              />
            </View>
          ) : (
            <Text style={[styles.refundNote, { color: colors.success, marginTop: 10 }]}>
              ✓ Deposit Refunded. Transaction Reference: {escrow.refundTxId}
            </Text>
          )}
        </Card>
      )}

      {/* Shipping Address */}
      <Card style={styles.card}>
        <Text style={[styles.sectionHeading, { color: colors.textPrimary }]}>Shipping & Rental Contact</Text>
        <Text style={[styles.addrText, { color: colors.textSecondary }]}>Thaha Hussain</Text>
        <Text style={[styles.addrText, { color: colors.textSecondary }]}>Flat 402, Sunset Towers, Bandra West</Text>
        <Text style={[styles.addrText, { color: colors.textSecondary }]}>Mumbai, Maharashtra - 400050</Text>
      </Card>

      <Button
        title="Download Tax Invoice (PDF)"
        variant="outline"
        size="lg"
        icon={<Download size={18} color={colors.accent} />}
        onPress={() => Alert.alert('Invoice Downloaded', 'Tax invoice PDF generated.')}
        style={{ marginVertical: 10 }}
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingTop: 68,
    paddingBottom: 110,
  },
  header: {
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
  },
  orderId: {
    fontSize: 14,
    fontWeight: '700',
    marginTop: 2,
  },
  card: {
    marginBottom: 14,
    padding: 16,
    borderRadius: 16,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusMeta: {
    flex: 1,
    marginLeft: 12,
  },
  statusTitle: {
    fontSize: 15,
    fontWeight: '700',
  },
  statusSub: {
    fontSize: 12,
    marginTop: 2,
  },
  escrowHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  escrowTitle: {
    fontSize: 15,
    fontWeight: '800',
    marginLeft: 8,
  },
  escrowRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 4,
  },
  escrowLabel: {
    fontSize: 13,
  },
  escrowValue: {
    fontSize: 16,
    fontWeight: '800',
  },
  refundNote: {
    fontSize: 12,
    fontWeight: '700',
  },
  sectionHeading: {
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 8,
  },
  addrText: {
    fontSize: 13,
    marginVertical: 2,
  },
});
